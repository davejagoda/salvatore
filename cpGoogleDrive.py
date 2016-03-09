#!/usr/bin/env python

import argparse
import time
import httplib2
import apiclient.discovery
import oauth2client.client

def uploadDrive(drive_service, filenames, folder, verbose=False, ocr=False):
    number_of_files_uploaded = 0
    # find directory
    q = 'title="{}"'.format(folder)
    files = drive_service.files().list(q=q).execute()
    if 1 != len(files['items']):
        print('did not find exactly one folder')
        return(None)
    id = files['items'][0]['id']
    # upload
    for filename in filenames:
        media_body = apiclient.http.MediaFileUpload(filename)
        body = {
            'title': filename,
            'description': filename,
            'parents': [{'id': id}]
        }
        # Perform the request and print the result.
        tries = 0
        done = False
        while not done and tries < 3:
            try:
                new_file = drive_service.files().insert(body=body, media_body=media_body, ocr=ocr).execute()
                done = True
                number_of_files_uploaded += 1
                if verbose:
                    print('successfully uploaded file with id:{} and name:{}'.format(new_file['id'], filename))
            except Exception as e:
                tries += 1
                print('on try:{} caught:{} exception while uploading:{}, retrying in {} seconds.'.format(tries, e, filename, 2 ** tries))
                time.sleep(2 ** tries)
    return(number_of_files_uploaded)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose output')
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-o', '--ocr', action='store_true', help='perform OCR on the uploaded file')
    parser.add_argument('filename', nargs='+', help='the path to the file[s] to be uploaded')
    parser.add_argument('folder', nargs=1, help='the Google Drive folder in which to upload')
    args = parser.parse_args()
    if args.verbose:
        print('filename[s]:{}'.format(args.filename))
        print('folder:{}'.format(args.folder))
        print('number of files:{}'.format(len(args.filename)))
    with open(args.tokenFile, 'r') as f:
        credentials = oauth2client.client.Credentials.new_from_json(f.read())
    if args.verbose:
        print(type(credentials))
        print(credentials)
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = apiclient.discovery.build('drive', 'v2', http=http)
    assert 1 == len(args.folder)
    print('{} files successfully uploaded'.format(uploadDrive(drive_service, args.filename, args.folder[0], args.verbose, args.ocr)))
