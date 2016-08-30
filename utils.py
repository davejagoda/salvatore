#!/usr/bin/env python

import httplib2
import apiclient.discovery
import oauth2client.client

def get_drive_service(tokenFile, verbose=0):
    with open(tokenFile, 'r') as f:
        credentials = oauth2client.client.Credentials.new_from_json(f.read())
    http = httplib2.Http()
    credentials.authorize(http)
    return(apiclient.discovery.build('drive', 'v2', http=http))

def get_folder_id(drive_service, folder, verbose=0):
    q = 'title="{}" and mimeType="application/vnd.google-apps.folder"'.format(folder)
    files = drive_service.files().list(q=q).execute()
    if 1 != len(files['items']):
        print('did not find exactly one folder')
        return(None)
    return(files['items'][0]['id'])

def get_document_contents_from_drive(drive_service, file_id, verbose=0):
    data = drive_service.files().export(fileId=file_id, mimeType='text/plain').execute().decode('utf8')
    assert(unichr(0xfeff) == data[0])
    if verbose > 0:
        print('BOM found')
    return(data[1:])

def get_document_title_and_type_from_id(drive_service, id, verbose=0):
    data = drive_service.files().get(fileId=id).execute()
    return(data['title'], data['mimeType'])
