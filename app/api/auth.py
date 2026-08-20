from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.models import get_db, User
from app.schemas import SUser, SUserLog, SUserPubluc
from app.crud import reg_user, log_user, set_cookie, del_cookie
from app.dependencies import get_user_by_request_strict

router = APIRouter()

@router.post('/register')
def post_register(response: Response, data: SUser, db: Session = Depends(get_db)):
    user = reg_user(data, db)
    cooke = set_cookie(db, user)

    response.set_cookie(
        key='session_id',
        value=cooke.session_id,
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite='lax',
        path='/'
    )
    
    return {'ok': True}

@router.post('/login')
def post_login(response: Response, data: SUserLog, db: Session = Depends(get_db)):
    user = log_user(data, db)
    cooke = set_cookie(db, user)

    response.set_cookie(
        key='session_id',
        value=cooke.session_id,
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite='lax',
        path='/'
    )

    return SUserPubluc.model_validate(user)

@router.post('/logout')
def post_logout(response: Response, request: Request, db: Session = Depends(get_db), user: User = Depends(get_user_by_request_strict)):
    del_cookie(db, request.cookies.get('session_id'))
    response.delete_cookie(key='session_id')
    return {'ok': True}