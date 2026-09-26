from app.models import SqlAlchemyBase
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from datetime import datetime, timezone


def _default_created_at():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _default_expires_at():
    from app.core import get_session_expiry
    return get_session_expiry().replace(tzinfo=None)


class Session(SqlAlchemyBase):
    __tablename__ = 'sessions'

    session_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=_default_created_at)
    expires_at = Column(DateTime, default=_default_expires_at, index=True)
