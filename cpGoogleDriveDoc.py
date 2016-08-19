#!/usr/bin/env python

import argparse
import apiclient
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

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('filename', help='the path to the file to be uploaded')
    args = parser.parse_args()
    drive_service = get_drive_service(args.tokenFile, args.verbose)
    print(uploadDrive(drive_service, args.filename))
