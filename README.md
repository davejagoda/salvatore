Salvatore
=========

Salvatore saves things (e.g. log files)

Installation
------------

```
cd ~/src/github
git clone git@github.com:davejagoda/salvatore.git
cd salvatore
pipenv install
```

Storage as a Service
--------------------

Google Drive

Amazon S3

Log files
---------

syslog ( `/var/log/syslog` )

http logs ( `/var/log/apache2/` )

Resources
---------

### Google

https://developers.google.com/accounts/docs/OAuth2InstalledApp

https://developers.google.com/accounts/docs/OAuth2ForDevices

https://developers.google.com/drive/web/quickstart/quickstart-python

https://developers.google.com/api-client-library/python/apis/drive/v2

https://developers.google.com/drive/v2/reference

### Amazon

http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html

http://docs.aws.amazon.com/cli/latest/reference/s3api/index.html

https://github.com/boto/boto3

### Mime types

https://developers.google.com/drive/v3/web/mime-types

http://www.iana.org/assignments/media-types/media-types.xhtml


Sample Invocations
------------------

Upload a test CSV file and convert it to a Google spreadsheet:

```
pipenv run ./cpGoogleDriveDoc.py -t oauth_token.json testfile testfolder -c
```

Upload a test text file and convert it to a Google document:

```
pipenv run ./cpGoogleDriveDoc.py -t oauth_token.json testfile testfolder -d
```
