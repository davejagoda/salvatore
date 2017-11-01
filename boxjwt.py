#!/usr/bin/env python

import argparse
import os
from boxsdk import JWTAuth, Client

def store_tokens(access_token, refresh_token):
    pass

auth = JWTAuth(
    client_id=os.getenv('BOX_CLIENT_ID'),
    client_secret=os.getenv('BOX_CLIENT_SECRET'),
    enterprise_id=os.getenv('BOX_ENTERPRISE_ID'),
    jwt_key_id=os.getenv('BOX_JWT_KEY_ID'),
    rsa_private_key_file_sys_path=os.getenv('BOX_PRIVATE_KEY_PEM_FILE'),
    store_tokens=store_tokens
)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--make_folder', help='make a folder')
    parser.add_argument('-u', '--upload_file', help='upload a file')
    parser.add_argument('-v', '--verbose', action='count', help='be verbose')
    args = parser.parse_args()

    client = Client(auth)
    if args.verbose > 0:
        me = client.user(user_id='me').get()
        print 'user_login: ' + me['login']
    root_folder = client.folder(folder_id='0').get()
    if args.verbose > 0:
        print 'folder owner: ' + root_folder.owned_by['login']
        print 'folder name: ' + root_folder['name']
    if args.make_folder:
        root_folder.create_subfolder(args.make_folder)
    if args.upload_file:
        root_folder.upload(args.upload_file)
    items = client.folder(folder_id='0').get_items(limit=100, offset=0)
    for item in items:
        print item
