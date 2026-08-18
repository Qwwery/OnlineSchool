from fastapi import APIRouter, Depends, Response
from app.models import get_db
from sqlalchemy.orm import Session
from app.schemas import SUser, SUserLog
from app.crud import reg_user, log_user

router = APIRouter()

@router.post('/reg')
def post_reg(response: Response, data: SUser, db: Session = Depends(get_db)):
    result = reg_user(data, db)

    response.set_cookie(
        key='session_id',
        value=result.session_id,
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite='lax',
        path='/'
    )
    
    return {'ok': True}

@router.post('/log')
def post_log(response: Response, data: SUserLog, db: Session = Depends(get_db)):
    result = log_user(data, db)

    response.set_cookie(
        key='session_id',
        value=result.session_id,
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite='lax',
        path='/'
    )

    return result
