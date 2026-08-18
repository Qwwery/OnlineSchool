from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.user import router as user_router
from app.web.course import router as course_router
from app.api.user import router as user_api_router
from app.api.course import router as course_api_router

from app.models.db_session import global_init
from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
db_patch = os.getenv('db_patch')
global_init(db_patch)

os.path.dirname(db_patch)

app = FastAPI()
app.mount(
    '/static',
    StaticFiles(directory=BASE_DIR / 'app' / 'static'),
    name='static'
)
app.include_router(router=user_router)
app.include_router(router=course_router)
app.include_router(router=user_api_router, tags=['users'])
app.include_router(router=course_api_router, prefix='/course', tags=['course'])
