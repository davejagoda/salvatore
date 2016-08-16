#!/usr/bin/env python

import boto3
s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
    for obj in bucket.objects.all():
        assert bucket.name == obj.bucket_name
        print(' {}'.format(obj.key))
