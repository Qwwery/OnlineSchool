from .db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class Course(SqlAlchemyBase):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    

