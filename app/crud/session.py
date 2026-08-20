from app.models import User, Session as CSession
from sqlalchemy.orm import Session

# Получение пользователя из бд по ссессии из куки
def get_user_by_session_id(db: Session, session_id : str) -> User:
    session = db.query(CSession).filter(CSession.session_id == session_id).first()
    user = db.query(User).filter(User.id == session.user_id).first()
    return user
