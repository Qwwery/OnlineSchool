from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.models import Course, get_db, User
from app.crud import all_course, new_course, get_course_by_id, user_hav_access_course
from app.dependencies import get_user_by_request_strict


def get_course_by_request_strict(course_id: int, db: Session = Depends(get_db), curent_user: User = Depends(get_user_by_request_strict)):
    if not curent_user:
        return None

    course = get_course_by_id(db, course_id)
    access = user_hav_access_course(db, curent_user.id, course_id)
    return {'course': course, 'access': access}
