from sqlalchemy.orm import Session
from app.models import Enrollment, Course

def create_enrollment(db: Session, user_id: int, course_id: int) -> Enrollment:
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def user_hav_access_course(db: Session, user_id: int, course_id: int) -> bool:
    enrollment = db.query(Enrollment).filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if course and course.author_id == user_id:
        return True

    return enrollment is not None
