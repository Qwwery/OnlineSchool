from .db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class Course(SqlAlchemyBase):
    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    description = Column(Text)
    image_url = Column(Text)
    price = Column(Integer, nullable=True)
    created_at = Column(DateTime, datetime.now())


