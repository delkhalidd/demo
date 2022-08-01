import sys, os
from PIL import Image
import json
import boto3
import botocore
#import time

def lambda_handler(event, context):
    KEY = event['Records'][0]['s3']['object']['key']
    BUCKET_NAME = event['Records'][0]['s3']['bucket']['name']
    file_path = '/tmp/'+KEY
    exif_file_path = '/tmp/exit1.jpg'
    DEST_BUCKET_NAME = "testuser0897"

    s3 = boto3.resource('s3')

    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, file_path)
        im = Image.open(file_path)
        # this clears all exif data
        im.getexif().clear()
        im.save(exif_file_path)
        #time.sleep(3)

        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(exif_file_path, DEST_BUCKET_NAME, KEY)
        
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print("ERROR")
            raise
    except Exception as e:
        print("Code Error")