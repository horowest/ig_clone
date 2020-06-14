import os
import boto3

S3_BUCKET = os.environ['S3_BUCKET']
S3_ACCESS_KEY = os.environ['S3_ACCESS_KEY']
S3_SECRET_KEY = os.environ['S3_SECRET_KEY']

def get_bucket():
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY) 
    loc = s3_client.get_bucket_location(Bucket=S3_BUCKET)['LocationConstraint']
    return loc

S3_BUCKET_LOC = get_bucket()