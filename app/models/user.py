from sqlalchemy import Column, Integer, String, Boolean
from .db_session import SqlAlchemyBase
import bcrypt

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_teacher = Column(Boolean, default=False)

    def check_password(self, password: str,) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )

