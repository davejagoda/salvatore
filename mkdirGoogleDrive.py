#!/usr/bin/env python

import argparse
import apiclient
import utils

def mkdir(drive_service, dirname):
    body = {
        'title': dirname,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    return(drive_service.files().insert(body=body).execute()['id'])

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('dirname', help='the directory to be created')
    args = parser.parse_args()
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    print(mkdir(drive_service, args.dirname))
