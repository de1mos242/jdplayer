import boto3
from botocore.config import Config


class FileService():

    def __init__(self) -> None:
        self.s3 = None
        self.bucket_name = None

    def init_app(self, url, client_id, secret_key, region, bucket_name):
        self.s3 = boto3.resource('s3',
                                 endpoint_url=url,
                                 aws_access_key_id=client_id,
                                 aws_secret_access_key=secret_key,
                                 config=Config(signature_version='s3v4'),
                                 region_name=region)
        self.bucket_name = bucket_name

    def upload_file(self, filepath, s3_name):
        bucket = self.s3.Bucket(self.bucket_name)
        bucket.upload_file(filepath, s3_name)

    def download_file(self, s3_name, filepath):
        bucket = self.s3.Bucket(self.bucket_name)
        bucket.download_file(s3_name, filepath)
