from sqlalchemy.orm import Session
from app.models import Video

def create_video(db: Session, s3_key: str, filename: str, size_bytes: int, user_id: int, course_id: int) -> Video:
    video = Video(key=s3_key, origin_name=filename, size_bytes=size_bytes, uploaded_by_user_id=user_id, course_id=course_id)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

def get_video_by_id(db: Session, video_id: int) -> Video:
    return db.query(Video).filter(Video.id == video_id).first()
