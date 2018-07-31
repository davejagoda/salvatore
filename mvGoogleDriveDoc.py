#!/usr/bin/env python

import argparse
import apiclient
import difflib
import codecs
import os
import sys
import utils

def uploadDrive(drive_service, filename, folder_id):
    body = {
        'title': filename,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [{'id': folder_id}]
    }
    media_body = apiclient.http.MediaFileUpload(filename,
                                 mimetype='text/plain',
                                 resumable=True
    )
    return(drive_service.files().insert(body=body,
                                        media_body=media_body).execute()['id'])

def diffOriginalVsDrive(original_document_contents, drive_document_contents):
    difflines_shown = False
    for line in difflib.unified_diff(original_document_contents,
                                     drive_document_contents):
        difflines_shown = True
        print(line)
    if not difflines_shown:
        print('files are same, showing remote file:')
        for line in drive_document_contents:
            print(line)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', required=True,
                        help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='show verbose output')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='allow user interaction')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='delete original file')
    parser.add_argument('filename', help='path to the file to be uploaded')
    parser.add_argument('folder', help='Google Drive folder in which to upload')
    args = parser.parse_args()
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    folder_id = utils.get_folder_id(drive_service, args.folder, args.verbose)
    if None == folder_id:
        sys.exit(1)
    file_id = uploadDrive(drive_service, args.filename, folder_id)
    if args.interactive:
        input('press enter to continue ')
    with codecs.open(args.filename, 'r', encoding='utf8') as f:
        original_document_contents = f.read()
    drive_document_contents = utils.get_document_contents_from_drive(
        drive_service, file_id, args.verbose)
    diffOriginalVsDrive(original_document_contents.splitlines(),
                        drive_document_contents.splitlines())
    if args.delete:
        response = input('enter "y" delete original file ')
        if 'y' == response:
            os.unlink(args.filename)
