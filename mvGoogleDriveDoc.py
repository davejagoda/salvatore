#!/usr/bin/env python

import argparse
import apiclient
import difflib
import codecs
import os
from utils import get_drive_service

def uploadDrive(drive_service, filename):
    body = {
        'title': filename,
        'mimeType': 'application/vnd.google-apps.document'
    }
    media_body = apiclient.http.MediaFileUpload(filename,
                                 mimetype='text/plain',
                                 resumable=True
    )
    return(drive_service.files().insert(body=body, media_body=media_body).execute()['id'])

def downloadDrive(drive_service, file_id):
    data = drive_service.files().export(fileId=file_id, mimeType='text/plain').execute().decode('utf8')
    assert(unichr(0xfeff) == data[0])
    print('BOM found')
    return(data[1:])

def diffOriginalVsDrive(original, drive):
    for line in difflib.unified_diff(original, drive):
        print(line)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('-i', '--interactive', action='store_true', help='allow user interaction')
    parser.add_argument('-d', '--delete', action='store_true', help='delete original file')
    parser.add_argument('filename', help='the path to the file to be uploaded')
    args = parser.parse_args()
    drive_service = get_drive_service(args.tokenFile, args.verbose)
    file_id = uploadDrive(drive_service, args.filename)
    if args.interactive:
        raw_input('press enter to continue ')
    with codecs.open(args.filename, 'r', encoding='utf8') as f:
        original = f.read()
    drive = downloadDrive(drive_service, file_id)
    diffOriginalVsDrive(original.splitlines(), drive.splitlines())
    if args.delete:
        response = raw_input('enter "y" delete original file ')
        if 'y' == response:
            os.unlink(args.filename)
