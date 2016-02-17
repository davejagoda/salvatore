#!/usr/bin/env python

import argparse
import httplib2
import apiclient.discovery
import oauth2client.client

def uploadDrive(drive_service, filename, folder, ocr=False):
    # find directory
    q = 'title="{}"'.format(folder)
    files = drive_service.files().list(q=q).execute()
    if 1 != len(files['items']):
        print('did not find exactly one folder')
        return(None)
    id = files['items'][0]['id']
    # upload
    media_body = apiclient.http.MediaFileUpload(filename)
    body = {
        'title': filename,
        'description': filename,
        'parents': [{'id': id}]
    }
    # Perform the request and print the result.
    new_file = drive_service.files().insert(body=body, media_body=media_body, ocr=ocr).execute()
    return(new_file['id'])

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose output')
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-o', '--ocr', action='store_true', help='perform OCR on the uploaded file')
    parser.add_argument('filename', help='the path to the file to be uploaded')
    parser.add_argument('folder', help='the Google Drive folder in which to upload')
    args = parser.parse_args()
    with open(args.tokenFile, 'r') as f:
        credentials = oauth2client.client.Credentials.new_from_json(f.read())
    if args.verbose:
        print(type(credentials))
        print(credentials)
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = apiclient.discovery.build('drive', 'v2', http=http)
    print(uploadDrive(drive_service, args.filename, args.folder, args.ocr))
