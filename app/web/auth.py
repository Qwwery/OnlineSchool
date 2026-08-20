from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import get_user_by_request_optional
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/register', response_class=HTMLResponse, tags=['users'])
async def get_register(request: Request, user: User = Depends(get_user_by_request_optional)):
    if user:
        return RedirectResponse('/', status_code=302)
    return templates.TemplateResponse(
        request=request,
        name='register.html'
    )

@router.get('/login', response_class=HTMLResponse, tags=['users'])
async def get_login(request: Request, user: User = Depends(get_user_by_request_optional)):
    if user:
        return RedirectResponse('/', status_code=302)
    return templates.TemplateResponse(
        request=request,
        name='login.html'
    )