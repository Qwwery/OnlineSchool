from sqlalchemy.orm import Session
from app.models import Video

def create_video(db: Session, s3_key: str, filename: str, size_bytes: int, user_id: int) -> Video:
    video = Video(key=s3_key, origin_name=filename, size_bytes=size_bytes, user_id=user_id)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

    