from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import get_db, User
from app.crud import create_enrollment
from app.dependencies import get_user_by_request_strict

router = APIRouter()

@router.post('/course/{course_id}')
def enroll_at_course_by_id(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_user_by_request_strict)):
    enroll = create_enrollment(db, current_user.id, course_id)
    if enroll:
        return {'ok': True}


