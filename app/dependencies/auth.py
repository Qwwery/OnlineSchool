from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.models import get_db, User
from app.crud import get_user_by_session_id

def get_user_by_request_strict(request: Request, db: Session = Depends(get_db)) -> User:
    session_id = request.cookies.get('session_id')

    if not session_id:
        raise HTTPException(401, 'Пользователь не авторизован')

    user = get_user_by_session_id(db, session_id)
    if not user:
        raise HTTPException(401, 'Сессия истекла')

    return user

def get_user_by_request_optional(request: Request, db: Session = Depends(get_db)) -> User | None:
    session = request.cookies.get('session_id')

    if not session:
        return None

    user = get_user_by_session_id(db, session)
    if not user:
        return None
    return user