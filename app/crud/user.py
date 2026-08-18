from app.models import User, Session as CSession
from ..schemas.user import SUser
from app.core import generat_session_id


from sqlalchemy.orm import Session
import bcrypt

from fastapi import HTTPException # Нет, не придумал как лучше. Плевать на единую ответственность

def cooke(db: Session, user: User) -> CSession:
    session_id = generat_session_id()
    session = CSession(
        session_id=session_id,
        user_id=user.id
    )


def reg_user(data: SUser, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail='Пользователь с такой почтой уже существует')
    password = data.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    db_user = User(
        name=data.name,
        email=data.email,
        password=hashed_password,
    )

    session = cooke(db, db_user)

    db.add(db_user)
    db.add(session)
    db.commit()
    db.refresh(db_user)
    return db_user

def log_user(data: SUser, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if not existing_user or not existing_user.check_password(data.password):
        raise HTTPException(status_code=401, detail='Неверный email или пароль')
    session = cooke(db, existing_user)
    return existing_user
