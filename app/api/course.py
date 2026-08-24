from app.schemas import SCourse
from app.models import Course, get_db, User
from app.crud import all_course, new_course
from app.dependencies import get_user_by_request_strict


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/add')
def post_course(course: SCourse, db: Session = Depends(get_db), curent_user: User = Depends(get_user_by_request_strict)):
    result = new_course(db, course, curent_user.id)
    return result
