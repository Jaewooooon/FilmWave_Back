# utils/S3ImageUploader.py
import boto3
from django.conf import settings
from uuid import uuid4

class S3ImageUploader:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_image(self, file, file_type):
        file_extension = file_type.split('/')[-1]
        file_name = f'group_images/{uuid4()}.{file_extension}'

        self.s3.upload_fileobj(
            file,
            self.bucket_name,
            file_name,
            ExtraArgs={
                'ContentType': file_type
            }
        )
        return f'https://{self.bucket_name}.s3.amazonaws.com/{file_name}'
