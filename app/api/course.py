from app.schemas import SCourse
from app.models import Course, get_db
from app.crud import all_course, new_course

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/add')
def post_course(course: SCourse, db: Session = Depends(get_db)):
    result = new_course(db, course)
    return result
