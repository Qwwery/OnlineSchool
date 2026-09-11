from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from app.models import Video, get_db
from app.schemas import SVideoUploadResponse, SVideoLinkResponse
from app.dependencies import get_user_by_request_strict
from app.services import generate_s3, validate_file_extension, upload_to_s3, generate_presigned_url
from app.crud import create_video, get_video_by_id, user_hav_access_course, is_author_course
from app.core import settings

router = APIRouter()

ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
MAX_SIZE_BYTES = 500 * 1024 * 1024

@router.post('/upload', response_model=SVideoUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_video(
    file: UploadFile = File(...),
    course_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_user_by_request_strict)
):
    if not validate_file_extension(file.filename or ""):
        raise HTTPException(400, detail="Недопустимый формат файла")

    if not is_author_course(db, current_user.id, course_id):
        raise HTTPException(404, detail="Курса нет, или нет прав на его изменение")


    file_stream = file.file # Это для BinaryIO
    contetn_type = file.content_type or "video/mp4"
    filename = file.filename    

    s3_key = generate_s3(current_user.id, filename)
    try:
        upload_to_s3(file_stream, s3_key, contetn_type)
    except Exception as e:
        raise HTTPException(500, detail="Ошибка загрузки")

    video = create_video(db, s3_key, filename, 0, current_user.id, course_id)
    return {'video_id': video.id, 'key': video.key}

@router.get('/{video_id}/link')
def get_video_link(video_id: int, db: Session = Depends(get_db), current_user = Depends(get_user_by_request_strict)):
    video = get_video_by_id(db, video_id)
    access = user_hav_access_course(db, current_user.id, video.course_id)
    if not video or not access:
        raise HTTPException(404, detail="Видео не найдено, или доступ запрещен")

    try:
        url = generate_presigned_url(video.key)
    except Exception as e:
        print(e)
        raise HTTPException(500, detail="Ошибка генерации URL")

    return {'url': url, "expires_in": settings.PRESIGNED_URL_EXPIRES}

@router.delete('/{video_id}/delete')
def delete_video(video_id: int, db: Session = Depends(get_db), current_user = Depends(get_user_by_request_strict)):
    pass

