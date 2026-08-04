from ..models.__all_models import User
from ..schemas.user import SUser
from sqlalchemy.orm import Session
import bcrypt

from fastapi import HTTPException # Нет, не придумал как лучше. Плевать на единую ответственность

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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def log_user(data: SUser, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if not existing_user or not existing_user.check_password(data.password):
        raise HTTPException(status_code=401, detail='Неверный email или пароль')
    return existing_user
