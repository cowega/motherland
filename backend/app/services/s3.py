import json
import boto3
from botocore.exceptions import ClientError
import anyio
from app.core.config import settings


class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION_NAME
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self.ensure_bucket_exists()

    def ensure_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code in ["404", "NoSuchBucket"] or (e.response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 404):
                self.client.create_bucket(Bucket=self.bucket_name)
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PublicReadGetObject",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                        }
                    ]
                }
                self.client.put_bucket_policy(
                    Bucket=self.bucket_name,
                    Policy=json.dumps(policy)
                )
            else:
                raise e

    def upload_file(self, file_data: bytes, file_name: str, content_type: str) -> str:
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=file_data,
            ContentType=content_type
        )
        return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{file_name}"


s3_service = S3Service()


async def upload_file_async(file_data: bytes, file_name: str, content_type: str) -> str:
    return await anyio.to_thread.run_sync(
        s3_service.upload_file,
        file_data,
        file_name,
        content_type
    )
