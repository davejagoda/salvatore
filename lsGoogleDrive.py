#!/usr/bin/env python

import argparse
import pprint
import utils

id_to_name_hash = {}

def list_drive(drive_service, name=None, pages_requested=0, verbose=0):
    pages_returned = 0
    result = []
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        if name:
            param['q'] = "title = '{}'".format(name)
        files = drive_service.files().list(**param).execute()
        result.extend(files['items'])
        page_token = files.get('nextPageToken')
        pages_returned += 1
        if verbose > 0:
            print('page {} returned'.format(pages_returned))
        if not page_token:
            break
        if pages_requested !=0 and pages_returned >= pages_requested:
            break
    return(result)

def print_raw_result(result):
    print('total {}'.format(len(result)))
    for item in result:
        pprint.pprint(item)

def get_name_from_id(drive_service, id, verbose=0):
    if id not in id_to_name_hash:
        (title, type) = utils.get_document_title_and_type_from_id(drive_service, id, verbose)
        id_to_name_hash[id] = title
    return(id_to_name_hash[id])

def print_result(drive_service, result, md5, count_parents, name_parents, verbose=0):
    for item in result:
        if md5:
            if 'md5Checksum' in item:
                sum = item['md5Checksum']
            else:
                sum = '0'*32
            print(u'{} {}'.format(sum, item['title']).encode('utf8'))
        if count_parents:
            print(u'{} {}'.format(len(item['parents']), item['title']).encode('utf8'))
        if name_parents:
            if 1 == len(item['parents']):
                print(u'{:32} {}'.format(get_name_from_id(drive_service, item['parents'][0]['id'], verbose), item['title']).encode('utf8'))
            if 0 == len(item['parents']):
                print(u'{:^32} {}'.format('None', item['title']).encode('utf8'))
            if 1 < len(item['parents']):
                print(u'{:^32} {}'.format('Multiple', item['title']).encode('utf8'))
        if not md5 and not count_parents and not name_parents:
            print(u'{}'.format(item['title']).encode('utf8'))

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('-p', '--pages', type=int, default=0, help='how many pages of results to show (omit to get all pages)')
    parser.add_argument('name', nargs='?', action='store', help='name to list')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--md5', action='store_true', help='show md5sums')
    group.add_argument('-c', '--count_parents', action='store_true', help='show parent counts')
    group.add_argument('-n', '--name_parents', action='store_true', help='show parent names')
    group.add_argument('-r', '--raw', action='store_true', help='show raw output')
    args = parser.parse_args()
    drive_service = utils.get_drive_service(args.tokenFile, args.verbose)
    result = list_drive(drive_service, args.name, args.pages, args.verbose)
    if args.raw:
        print_raw_result(result)
    else:
        print_result(drive_service, result, args.md5, args.count_parents, args.name_parents, args.verbose)
