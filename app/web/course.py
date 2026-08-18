from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.crud import all_course
from app.models import get_db


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    data = all_course(db)
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context= {
            'course': data
        })


@router.get('/course/add', response_class=HTMLResponse, tags=['course'])
async def get_add_course(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='add_course.html'
    )