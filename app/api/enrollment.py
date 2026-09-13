from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import get_db, User
from app.crud import create_enrollment, get_course_by_id, user_hav_access_course
from app.dependencies import get_user_by_request_strict

router = APIRouter()

@router.post('/course/{course_id}')
def enroll_at_course_by_id(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_user_by_request_strict)):
    course = get_course_by_id(db, course_id)
    if course.price > current_user.balance:
        raise HTTPException(402, "Payment Required")
    access = user_hav_access_course(db, current_user.id, course_id)
    if access:
        raise HTTPException(409, "Already bought")
    enroll = create_enrollment(db, current_user.id, course_id)
    if enroll:
        return {'ok': True}


