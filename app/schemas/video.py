from pydantic import BaseModel

class SVideoUploadResponse(BaseModel):
    video_id: int
    key: str

class SVideoLinkResponse(BaseModel):
    url: str
    expires_in: int

