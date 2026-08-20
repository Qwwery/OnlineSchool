from pydantic import BaseModel, ConfigDict


class SUser(BaseModel):
    name: str
    email: str
    password: str
    is_admin: bool = False
    is_teacher: bool = False

class SUserLog(BaseModel):
    email: str
    password: str

class SUserPubluc(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    is_admin: bool
    is_teacher: bool