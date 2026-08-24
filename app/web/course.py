from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import all_course
from app.models import get_db, User
from app.dependencies import get_user_by_request_optional


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