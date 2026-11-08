from app.models import User, Session as CSession
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Получение пользователя из бд по ссессии из куки
def get_user_by_session_id(db: Session, session_id : str) -> User:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    session = db.query(CSession).filter(
        CSession.session_id == session_id,
        (CSession.expires_at.is_(None)) | (CSession.expires_at > now),
    ).first()

    if session is None:
        # Сессии нет или она истекла — удаляем просроченные записи из базы
        purge_expired_sessions(db)
        return None

    user = db.query(User).filter(User.id == session.user_id).first()
    return user


def purge_expired_sessions(db: Session) -> int:
    """Удаляет из базы все записи сессий, у которых вышло время окончания."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    deleted = db.query(CSession).filter(
        CSession.expires_at.isnot(None),
        CSession.expires_at <= now,
    ).delete(synchronize_session=False)
    if deleted:
        db.commit()
    return deleted
