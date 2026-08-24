from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import Video, get_db
from app.schemas import SVideoUploadResponse, SVideoLinkResponse
from app.dependencies import get_user_by_request_strict
from app.services import generate_s3, validate_file_extension, upload_to_s3
from app.crud import create_video

router = APIRouter()

ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
MAX_SIZE_BYTES = 500 * 1024 * 1024

@router.post('api/upload', response_model=SVideoUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_user_by_request_strict)
):
    if not validate_file_extension(file.filename or ""):
        raise HTTPException(400, detal="Недопустимый формат файла")

    file_stream = file.file # Это для BinaryIO
    contetn_type = file.content_type or "video/mp4"
    filename = file.filename

    s3_key = generate_s3(current_user.id, filename)
    try:
        upload_to_s3(file_stream, s3_key, contetn_type)
    except Exception as e:
        raise HTTPException(500, detal="Ошибка загрузки")

    video = create_video(db, s3_key, filename, 0, current_user.id)
    return {'video_id': video.id, 'key': video.key}

