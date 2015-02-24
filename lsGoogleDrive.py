#!/usr/bin/env python

import pprint
import httplib2
import apiclient.discovery
import oauth2client.client

f = open('bearer_token.json', 'r')
credentials = oauth2client.client.Credentials.new_from_json(f.read())
f.close()
print(type(credentials))
print(credentials)

http = httplib2.Http()
credentials.authorize(http)
drive_service = apiclient.discovery.build('drive', 'v2', http=http)

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

print(len(result))
for item in result:
    pprint.pprint(item)
