import uuid
from typing import BinaryIO
from app.core import s3_client, settings

ALLOWED_EXTENSION = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

def generate_s3(user_id: int, filename: str) -> str:
    ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    return f"videos/{user_id}/{unique_filename}"

def validate_file_extension(filename: str) -> bool:
    ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""
    return ext in ALLOWED_EXTENSION

def upload_to_s3(
    file_stream: BinaryIO,
    s3_key: str,
    content_type: str = "video/mp4"
) -> None:
    s3_client.upload_fileobj(
        file_stream,
        settings.S3_BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": content_type},
    )

def generate_presigned_url(s3_key: str) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=settings.PRESIGNED_URL_EXPIRES,
    )
