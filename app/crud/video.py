from sqlalchemy.orm import Session
from app.models import Video
from typing import List, Dict


def create_video(db: Session, s3_key: str, filename: str, size_bytes: int, user_id: int, course_id: int) -> Video:
    count_video_at_course = db.query(Video).filter(Video.course_id == course_id).all()
    video = Video(
        key=s3_key, 
        origin_name=filename, 
        size_bytes=size_bytes, 
        uploaded_by_user_id=user_id, 
        course_id=course_id, 
        id_at_course=len(count_video_at_course)+1
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

def get_video_by_id(db: Session, video_id: int) -> Video:
    video = db.query(Video).filter(Video.id == video_id).first()
    return video

def get_videos_by_course_id(db: Session, course_id: int) -> List[Video]:
    return db.query(Video).filter(Video.course_id == course_id).all()

def delete_video_by_id(db: Session, video_id: int) -> Dict:
    video = get_video_by_id(db, video_id)
    db.delete(video)
    db.commit()
    return {'ok': True}