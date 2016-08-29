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
    return(drive_service.files().insert(body=body, media_body=media_body).execute()['id'])

def downloadDrive(drive_service, file_id, verbose=0):
    data = drive_service.files().export(fileId=file_id, mimeType='text/plain').execute().decode('utf8')
    assert(unichr(0xfeff) == data[0])
    if verbose > 0:
        print('BOM found')
    return(data[1:])

def diffOriginalVsDrive(original, drive):
    difflines_shown = False
    for line in difflib.unified_diff(original, drive):
        difflines_shown = True
        print(line)
    if not difflines_shown:
        print('files are same, showing remote file:')
        for line in drive:
            print(line)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('-i', '--interactive', action='store_true', help='allow user interaction')
    parser.add_argument('-d', '--delete', action='store_true', help='delete original file')
    parser.add_argument('filename', help='the path to the file to be uploaded')
    parser.add_argument('folder', help='the Google Drive folder in which to upload')
    args = parser.parse_args()
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    folder_id = utils.get_folder_id(drive_service, args.folder, args.verbose)
    if None == folder_id:
        sys.exit(1)
    file_id = uploadDrive(drive_service, args.filename, folder_id)
    if args.interactive:
        raw_input('press enter to continue ')
    with codecs.open(args.filename, 'r', encoding='utf8') as f:
        original = f.read()
    drive = downloadDrive(drive_service, file_id, args.verbose)
    diffOriginalVsDrive(original.splitlines(), drive.splitlines())
    if args.delete:
        response = raw_input('enter "y" delete original file ')
        if 'y' == response:
            os.unlink(args.filename)
