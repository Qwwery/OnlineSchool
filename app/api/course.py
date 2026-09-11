from app.schemas import SCourse
from app.models import Course, get_db, User
from app.crud import all_course, new_course, get_videos_by_course_id, delete_course, get_user_by_course_id
from app.dependencies import get_user_by_request_strict, get_course_by_request_strict


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/add')
def post_course(course: SCourse, db: Session = Depends(get_db), curent_user: User = Depends(get_user_by_request_strict)):
    result = new_course(db, course, curent_user.id)
    return result

@router.get('/{course_id}/see')
def get_course(course_id: int, db: Session = Depends(get_db), curent_user: User = Depends(get_user_by_request_strict), info_course: Course = Depends(get_course_by_request_strict)):
    access = info_course['access']
    course = info_course['course']
    videos_in_course = get_videos_by_course_id(db, course_id)
    author = get_user_by_course_id(db, course_id)
    
    return {'course': course, 'videos': videos_in_course, 'access': access, 'author': author}

@router.delete('/{course_id}/delete')
def delete_course(course_id: int, db: Session = Depends(get_db), curent_user: User = Depends(get_user_by_request_strict)):
    result = delete_course(db, course_id, curent_user.id)
    return result
