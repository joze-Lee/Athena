import boto3
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_pdf_to_s3(file_obj, filename):
    try:
        assert AWS_BUCKET_NAME is not None, "Bucket name not set in environment variables!"
        s3.upload_fileobj(file_obj, AWS_BUCKET_NAME, filename)
        return True
    except NoCredentialsError:
        return False

def get_presigned_url(filename, expiration=300):
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_BUCKET_NAME, 'Key': filename},
        ExpiresIn=expiration
    )
