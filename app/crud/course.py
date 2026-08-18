from app.models import Course
from sqlalchemy.orm import Session
from app.schemas import SCourse

def all_course(db: Session):
    course = db.query(Course).all()
    return course

def new_course(db: Session, data: SCourse):
    course = Course(name=data.title, description=data.description, price=data.price, image_url=data.image_path)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
