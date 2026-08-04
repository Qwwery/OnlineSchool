from pydantic import BaseModel

class SCourse(BaseModel):
    title: str
    description: str
    price: int
    image_path: str | None = None
    
