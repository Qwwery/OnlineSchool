from app.models import SqlAlchemyBase
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
import datetime

class Session(SqlAlchemyBase):
    __tablename__ = 'sessions'

    session_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
