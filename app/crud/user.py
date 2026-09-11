from sqlalchemy.orm import Session
from app.models import User, Course



def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    return user

def get_user_by_course_id(db: Session, course_id: int):
    user = db.query(User).join(Course).filter(Course.id == course_id).first()
    return user
