#!/usr/bin/env python

import argparse
import apiclient
import os
import sys
import utils

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', required=True,
                        help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='show verbose output')
    parser.add_argument('new_folder', help='the new folder')
    args = parser.parse_args()
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    new_id = utils.get_folder_id(drive_service, args.new_folder, args.verbose)
    if None == new_id:
        print('new_folder not found')
        sys.exit(1)
    root_id = utils.get_root_folder_id(drive_service, args.verbose)
    print(root_id)
    items = utils.get_folder_contents_from_id(drive_service, root_id,
                                              args.verbose)
    for item in items:
        if args.verbose:
            print('{}:{}:{}'.format(item['id'], item['mimeType'],
                                    item['title']))
        if 'application/vnd.google-apps.folder' == item['mimeType']:
            if args.verbose:
                print('folder, skipping')
        else:
            drive_service.files().update(fileId=item['id'],
                                         addParents=new_id,
                                         removeParents=root_id,
                                         fields='id, parents').execute()
