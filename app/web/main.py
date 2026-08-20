from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import Session, get_db, User
from app.crud import all_course
from app.dependencies import get_user_by_request_optional

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db), user: User = Depends(get_user_by_request_optional)):
    data = all_course(db)
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context= {
            'user': user,
            'courses': data
        })