from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import all_course
from app.models import get_db, User
from app.dependencies import get_user_by_request_optional, get_course_by_request_strict



router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/new', response_class=HTMLResponse)
async def get_new_course(request: Request, current_user: User = Depends(get_user_by_request_optional)):
    return templates.TemplateResponse(
        request=request,
        name='add_course.html',
        context= {'user': current_user}
    )

@router.get('/', response_class=HTMLResponse)
def get_all_course(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_user_by_request_optional)):
    courses = all_course(db)
    return templates.TemplateResponse(
            request=request,
            name='all_course.html',
            context= {'courses': courses, 'user': current_user}
        )

@router.get('/{course_id}', response_class=HTMLResponse)
async def get_course(request: Request, course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_user_by_request_optional)):
    course = get_course_by_request_strict(course_id, db, current_user)
    return templates.TemplateResponse(
            request=request,
            name='course_detal.html',
            context= {'course': course,
            'user': current_user, 
            "course_id": course_id,}
        )

# @router.get("/{course_id}/video/{video_id}") TODO
# def video_page(request: Request, course_id: int, video_id: int):
#     return templates.TemplateResponse(
#         request=request,
#         name = "video.html",
#         context=
#         {
#             "request": request,
#             "course_id": course_id,
#             "video_id": video_id,
#         },
#     )