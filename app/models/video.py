from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.models import SqlAlchemyBase

class Video(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False, unique=True)
    origin_name = Column(String, nullable=False)
    size_bytes = Column(Integer, default=0)
    uploaded_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))