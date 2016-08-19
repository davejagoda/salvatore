#!/usr/bin/env python

import argparse
import apiclient
from utils import get_drive_service

mime_dict = {
    'csv': ['application/vnd.google-apps.spreadsheet', 'text/csv'],
    'doc': ['application/vnd.google-apps.document', 'text/plain']
}

def uploadDrive(drive_service, filename, dict_key):
    body = {
        'title': filename,
        'mimeType': mime_dict[dict_key][0]
    }
    media_body = apiclient.http.MediaFileUpload(filename,
                                 mimetype=mime_dict[dict_key][1],
                                 resumable=True
    )
    return(drive_service.files().insert(body=body, media_body=media_body).execute()['id'])

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--csv', action='store_true', help='convert to google spreadsheet')
    group.add_argument('-d', '--doc', action='store_true', help='convert to google doc')
    parser.add_argument('filename', help='the path to the file to be uploaded')
    args = parser.parse_args()
    drive_service = get_drive_service(args.tokenFile, args.verbose)
    if args.csv:
        dict_key = 'csv'
    if args.doc:
        dict_key = 'doc'
    print(uploadDrive(drive_service, args.filename, dict_key))
