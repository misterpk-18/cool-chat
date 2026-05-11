import boto3
import uuid
import os


class UploadService:

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv(
            "AWS_ACCESS_KEY"
        ),
        aws_secret_access_key=os.getenv(
            "AWS_SECRET_KEY"
        ),
        region_name=os.getenv(
            "AWS_REGION"
        )
    )

    BUCKET_NAME = os.getenv(
        "AWS_BUCKET_NAME"
    )

    @staticmethod
    def upload_image(file):

        extension = file.filename.split(".")[-1]

        unique_filename = (
            str(uuid.uuid4())
            + "."
            + extension
        )

        UploadService.s3.upload_fileobj(
            file,
            UploadService.BUCKET_NAME,
            unique_filename,
            ExtraArgs={
                "ContentType":file.content_type
            }
        )

        image_url = f"https://{UploadService.BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

        return image_url