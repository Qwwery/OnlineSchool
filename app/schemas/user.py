from pydantic import BaseModel, ConfigDict


class SUserRegister(BaseModel):
    name: str
    email: str
    password: str

class SUserLogin(BaseModel):
    email: str
    password: str

class SUserPubluc(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    is_admin: bool
    is_teacher: bool