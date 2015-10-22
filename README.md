Salvatore
=========

Salvatore saves things (e.g. log files)

Installation
------------

cd ~/src/github
git clone git@github.com:a16z/salvatore.git
cd salvatore
virtualenv venv
source venv/bin/activate
pip install google-api-python-client
pip install boto3


Storage as a Service
--------------------

Google Drive
Amazon S3

Log files
---------

syslog ( /var/log/syslog )

http logs ( /var/log/apache2/ )

Resources
---------

https://developers.google.com/accounts/docs/OAuth2InstalledApp

https://developers.google.com/accounts/docs/OAuth2ForDevices

https://developers.google.com/drive/web/quickstart/quickstart-python

https://developers.google.com/api-client-library/python/apis/drive/v2

https://developers.google.com/drive/v2/reference

http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html

http://docs.aws.amazon.com/cli/latest/reference/s3api/index.html

https://github.com/boto/boto3
