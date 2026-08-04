from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from schemas import SUser, SUserLog
from models import get_db
from crud import reg_user, log_user, all_course


templates = Jinja2Templates(directory='app/templates')
router = APIRouter()

@router.get('/', response_class=HTMLResponse)
def index(request: Request):
    data = all_course
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context= {
            'course': data
        })

@router.get('/reg', response_class=HTMLResponse)
async def get_reg(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='reg.html'
    )

@router.post('/reg')
def post_reg(data: SUser, db: Session = Depends(get_db)):
    result = reg_user(data, db)
    return result

@router.get('/log', response_class=HTMLResponse)
async def get_log(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='log.html'
    )

@router.post('/log')
def post_log(data: SUserLog, db: Session = Depends(get_db)):
    result = log_user(data, db)
    return result

