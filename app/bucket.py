import os

from botocore.exceptions import ClientError
from botocore.response import StreamingBody
from dotenv import load_dotenv
from boto3 import Session


class FileBucket:
    load_dotenv()

    def __init__(self):
        self.s3 = Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION'),
        ).client("s3")
        self.bucket = os.getenv('AWS_BUCKET')

    def upload(self, file: bytes, filename: str):
        try:
            self.s3.put_object(
                Body=file,
                Bucket=self.bucket,
                Key=filename,
            )
        except ClientError:
            raise

    def download(self, filename: str) -> StreamingBody:
        return self.s3.get_object(
            Bucket=self.bucket,
            Key=filename,
        ).get("Body")

    def delete(self, filename: str):
        self.s3.delete_object(
            Bucket=self.bucket,
            Key=filename,
        )
