from pydantic import BaseModel


class SUser(BaseModel):
    name: str
    email: str
    password: str
    is_admin: bool = False
    is_teacher: bool = False

class SUserLog(BaseModel):
    email: str
    password: str
