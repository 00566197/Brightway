import boto3
import os
import uuid

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get('R2_ENDPOINT_URL'),
    aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
)

def upload_image(file, folder='cars'):
    ext = file.filename.rsplit('.', 1)[-1]
    filename = f"{folder}/{uuid.uuid4()}.{ext}"
    s3.upload_fileobj(
        file,
        os.environ.get('R2_BUCKET_NAME'),
        filename,
        ExtraArgs={'ContentType': file.content_type}
    )
    return f"{os.environ.get('R2_PUBLIC_URL')}/{filename}"