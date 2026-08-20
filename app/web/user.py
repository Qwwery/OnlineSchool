from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import User, get_db
from app.dependencies import get_user_by_request_strict
from app.crud import get_user_by_id


templates = Jinja2Templates(directory='app/templates')
router = APIRouter()

@router.get('/profile', response_class=HTMLResponse, tags=['user'])
async def get_profile(request: Request, user: User = Depends(get_user_by_request_strict)):
    return templates.TemplateResponse(
        request=request,
        name='profile_me.html',
        context={
            'user': user
        }
    )

@router.get('/profile/{profile_id}', response_class=HTMLResponse, tags=['user'])
def get_profile_by_id(profile_id: int, request: Request, user: User = Depends(get_user_by_request_strict), db: Session = Depends(get_db)):
    sear_user = get_user_by_id(profile_id, db)
    if not sear_user:
        raise HTTPException(404, 'Пользователь не найден')
    return templates.TemplateResponse(
        request=request,
        name='profile.html',
        context={
            'user': sear_user,
        }
    )
