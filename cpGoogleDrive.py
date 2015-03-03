#!/usr/bin/env python

import sys
import httplib2
import apiclient.discovery
import oauth2client.client

if 3 != len(sys.argv):
    print('need two arguments - the file to upload and the destination folder')
    sys.exit(1)
filename = sys.argv[1]
folder = sys.argv[2]

f = open('bearer_token.json', 'r')
credentials = oauth2client.client.Credentials.new_from_json(f.read())
f.close()

http = httplib2.Http()
credentials.authorize(http)
drive_service = apiclient.discovery.build('drive', 'v2', http=http)

# find directory
q="title='" + folder + "'"
files = drive_service.files().list(q=q).execute()
if 1 != len(files['items']):
    print('did not find exactly one folder')
    sys.exit(1)
id = files['items'][0]['id']

# upload
media_body = apiclient.http.MediaFileUpload(
    filename,
    mimetype = 'text/plain'
)

body = {
  'title': filename,
  'description': filename,
  'parents': [{'id': id}]
}

# Perform the request and print the result.
new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
print(new_file['id'])
