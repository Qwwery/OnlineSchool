from sqlalchemy.orm import Session
from app.models import User, Session as CSession
from app.core import generate_session_id

from fastapi import HTTPException

def set_cookie(db: Session, user: User) -> CSession:
    session_id = generate_session_id()
    session = CSession(
        session_id=session_id,
        user_id=user.id
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def del_cookie(db: Session, session_id: str):
    session = db.query(CSession).filter(CSession.session_id == session_id).first()
    if not session:
        raise HTTPException(404, 'Сессия не найдена')
    db.delete(session)
    db.commit()
    return {'ok': True}