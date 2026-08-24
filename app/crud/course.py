from app.models import Course
from sqlalchemy.orm import Session
from app.schemas import SCourse

def all_course(db: Session):
    course = db.query(Course).all()
    return course

def new_course(db: Session, data: SCourse, author_id: int):
    course = Course(name=data.title, description=data.description, price=data.price, image_url=data.image_path, author_id=author_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def is_author_course(db: Session, user_id: int, course_id: int):
    return db.query(Course).filter(Course.id == course_id, Course.author_id == user_id).first() is not None
