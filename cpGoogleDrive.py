#!/usr/bin/env python

import argparse
import time
import apiclient
import utils

def uploadDrive(drive_service, filenames, folder_id, verbose=False, ocr=False, ocrLanguage=None):
    number_of_files_uploaded = 0
    for filename in filenames:
        media_body = apiclient.http.MediaFileUpload(filename)
        body = {
            'title': filename,
            'description': filename,
            'parents': [{'id': folder_id}]
        }
        # Perform the request and print the result.
        tries = 0
        done = False
        while not done and tries < 3:
            try:
                new_file = drive_service.files().insert(
                    body=body,
                    media_body=media_body,
                    ocr=ocr,
                    ocrLanguage=ocrLanguage
                ).execute()
                done = True
                number_of_files_uploaded += 1
                if verbose:
                    print('successfully uploaded file with id:{} and name:{}'.
                          format(new_file['id'], filename))
            except Exception as e:
                tries += 1
                print('on try:{} caught:{} exception while uploading:{}, retrying in {} seconds.'.format(tries, e, filename, 2 ** tries))
                time.sleep(2 ** tries)
    return(number_of_files_uploaded)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True,
                        help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count',
                        help='show verbose output')
    parser.add_argument('-o', '--ocr', action='store_true',
                        help='perform OCR on the uploaded file')
    parser.add_argument('-l', '--ocrLanguage', action='store',
                        help='ocr language hint (e.g. "en")')
    parser.add_argument('filename', nargs='+',
                        help='the path to the file[s] to be uploaded')
    parser.add_argument('folder', nargs=1,
                        help='the Google Drive folder in which to upload')
    args = parser.parse_args()
    if args.verbose:
        print('filename[s]:{}'.format(args.filename))
        print('folder:{}'.format(args.folder))
        print('number of files:{}'.format(len(args.filename)))
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    assert 1 == len(args.folder)
    folder_id = utils.get_folder_id(drive_service, args.folder[0], args.verbose)
    if folder_id is None:
        print('folder {} not found'.format(args.folder[0]))
    else:
        print('{} files successfully uploaded'.format(uploadDrive(
            drive_service, args.filename, folder_id, args.verbose,
            args.ocr, args.ocrLanguage
        )))
