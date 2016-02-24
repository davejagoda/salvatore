#!/usr/bin/env python

import argparse
import pprint
import httplib2
import apiclient.discovery
import oauth2client.client

def get_drive_service(tokenFile, verbose=0):
    with open(tokenFile, 'r') as f:
        credentials = oauth2client.client.Credentials.new_from_json(f.read())
    http = httplib2.Http()
    credentials.authorize(http)
    return(apiclient.discovery.build('drive', 'v2', http=http))

def list_drive(drive_service, verbose=0):
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

def print_raw_result(result):
    print('total {}'.format(len(result)))
    for item in result:
        pprint.pprint(item)

def print_names(result):
    names = []
    for item in result:
        names.append(item['title'])
    names.sort()
    for name in names:
        print(name.encode('utf8'))

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-r', '--raw', action='store_true', help='show raw output')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    args = parser.parse_args()
    drive_service = get_drive_service(args.tokenFile, args.verbose)
    result = list_drive(drive_service, args.verbose)
    if args.raw:
        print_raw_result(result)
    else:
        print_names(result)
