#!/usr/bin/env python

import argparse
import os
import errno
from boxsdk import JWTAuth, Client

auth = JWTAuth(
    client_id=os.environ['BOX_CLIENT_ID'],
    client_secret=os.environ['BOX_CLIENT_SECRET'],
    enterprise_id=os.environ['BOX_ENTERPRISE_ID'],
    jwt_key_id=os.environ['BOX_JWT_KEY_ID'],
    rsa_private_key_data=os.environ['BOX_PRIVATE_KEY_PEM']
)

# af_id == ancestor_folder_id

def folder_from_name(folder_name, af_id, verbose):
    folder_id = None
    for item in find_items(folder_name, af_id, True, verbose):
        if None == folder_id or int(folder_id) < int(item['id']):
            folder_id = item['id']
    if None == folder_id:
        return('0')
    else:
        return(folder_id)

def print_item(item, indent):
    if 'folder' == item.type:
        symbol = '+'
    else:
        symbol = '-'
    print('{}{} id:{} name:{}'.format('.'*indent, symbol, item.id, item.name))

def list_folder(folder_id, indent, recursive=False):
    for item in client.folder(folder_id=folder_id).get_items(limit=100,
                                                             offset=0):
        assert(item.type in ['file', 'folder'])
        print_item(item, indent)
        if recursive and 'folder' == item.type:
            list_folder(item.id, indent+1, recursive)

def find_items(query, af_id, exact, verbose):
    items = []
    ancestor_folder = client.folder(folder_id=af_id)
    for item in client.search(query='"{}"'.format(query), limit=100, offset=0,
                              ancestor_folders=[ancestor_folder],
                              content_types=['name']):
        if verbose > 0:
            print_item(item, indent=0)
        if item.name == query or not exact:
            items.append(item)
    return(items)

def delete_item(item_name, af_id, verbose):
    items = find_items(item_name, af_id, True, verbose)
    if 1 != len(items):
        print('did not find exactly one item, no delete will occur')
    else:
        item_id = items[0]['id']
        print('deleting:{}'.format(item_id))
        if 'folder' == items[0]['type']:
            client.folder(item_id).delete(recursive=False)
        else:
            client.file(item_id).delete()

def make_folder(folder_name, folder_id, verbose):
    if verbose > 0:
        print('creating folder:{} in folder_id:{}'.format(folder_name, folder_id))
    client.folder(folder_id=folder_id).create_subfolder(folder_name)

def upload_file(file_name, folder_id, verbose):
    if verbose > 0:
        print('uploading file:{} to folder_id:{}'.format(file_name, folder_id))
    client.folder(folder_id=folder_id).upload(file_name)

def get_file(file_name, folder_id, verbose):
    if verbose > 0:
        print('getting file:{} from folder_id:{}'.format(file_name, folder_id))
    items = find_items(file_name, folder_id, True, verbose)
    if 1 != len(items):
        print('did not find exactly one item, not getting file')
    else:
        file_id = items[0]['id']
# don't overwrite a local file
# https://stackoverflow.com/questions/10978869/safely-create-a-file-if-and-only-if-it-does-not-exist-with-python
        try:
            fh = os.open(file_name, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('local file exists, will not overwrite')
            else:
                raise
        else:
            with os.fdopen(fh, 'w') as file_obj:
                client.file(file_id=file_id).download_to(file_obj)

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--ancestor', help='ancestor folder to use')
    parser.add_argument('-d', '--delete', help='delete an item')
    parser.add_argument('-g', '--get_file', help='get a file')
    parser.add_argument('-l', '--list', action='store_true', help='list all')
    parser.add_argument('-m', '--make_folder', help='make a folder')
    parser.add_argument('-u', '--upload_file', help='upload a file')
    parser.add_argument('-s', '--search', help='search for an item')
    parser.add_argument('-v', '--verbose', action='count', help='be verbose')
    args = parser.parse_args()

    client = Client(auth)
    if args.verbose > 1:
        me = client.user(user_id='me').get()
        print('user_login: ' + me['login'])
    root_folder = client.folder(folder_id='0').get()
    if args.verbose > 1:
        print('folder owner: ' + root_folder.owned_by['login'])
        print('folder name:{} folder id:{}'.format(root_folder['name'],
                                                   root_folder['id']))
    if args.ancestor:
        af_id = folder_from_name(args.ancestor, af_id='0', verbose=args.verbose)
    else:
        af_id = '0'
    if args.delete:
        delete_item(args.delete, af_id, args.verbose)
    if args.get_file:
        get_file(args.get_file, af_id, args.verbose)
    if args.list:
        list_folder(af_id, indent=0, recursive=True)
    if args.make_folder:
        make_folder(args.make_folder, af_id, args.verbose)
    if args.upload_file:
        upload_file(args.upload_file, af_id, args.verbose)
    if args.search:
        print('search results for name:{}'.format(args.search))
        for item in find_items(args.search, af_id, True, args.verbose):
            print_item(item, 0)
