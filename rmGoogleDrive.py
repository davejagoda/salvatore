#!/usr/bin/env python

import argparse
import difflib
import codecs
import os
import sys
import utils

def get_file_ids(drive_service, filename, verbose=0):
    q = 'title="{}" and mimeType="application/vnd.google-apps.document"'.format(filename)
    files = drive_service.files().list(q=q).execute()
    if verbose > 0:
        print(len(files['items']))
    results = []
    for item in files['items']:
        results.append(item['id'])
    return(results)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('filename', help='the name of the file to be deleted')
    args = parser.parse_args()
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    for file_id in get_file_ids(drive_service, args.filename, args.verbose):
        print('file id:{}'.format(file_id))
        print(utils.get_document_contents_from_drive(drive_service, file_id, args.verbose))
        response = raw_input('enter "y" delete file ')
        if 'y' == response:
            print(drive_service.files().delete(fileId=file_id).execute())
