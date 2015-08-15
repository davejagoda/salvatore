#!/usr/bin/env python

import argparse
import pprint
import httplib2
import apiclient.discovery
import oauth2client.client

def listDrive(drive_service):
    result = []
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = drive_service.files().list(**param).execute()
        result.extend(files['items'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    return(result)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose output')
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    args = parser.parse_args()
    with open(args.tokenFile, 'r') as f:
        credentials = oauth2client.client.Credentials.new_from_json(f.read())
    if args.verbose:
        print(type(credentials))
        print(credentials)
    http = httplib2.Http()
    credentials.authorize(http)
    result = listDrive(apiclient.discovery.build('drive', 'v2', http=http))
    print('total {}'.format(len(result)))
    for item in result:
        pprint.pprint(item)
