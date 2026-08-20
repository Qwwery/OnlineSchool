from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.crud import all_course
from app.models import get_db


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/new', response_class=HTMLResponse, tags=['course'])
async def get_new_course(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='add_course.html'
    )

@router.get('/', response_class=HTMLResponse, tags=['course'])
def get_all_course(request: Request, db: Session = Depends(get_db)):
    courses = all_course(db)
    return templates.TemplateResponse(
            request=request,
            name='all_course.html',
            context= {'courses': courses}
        )