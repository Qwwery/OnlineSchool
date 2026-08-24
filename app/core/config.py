from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str
    S3_ENDPOINT_URL: str
    S3_REGION: str = "us-east-1"
    PRESIGNED_URL_EXPIRES: int = 3600 
    db_patch: str

    class Config:
        env_file = '.env'

settings = Settings()
