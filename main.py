from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web import user_router, auth_router, course_router, main_router
from app.api import api_auth_router, api_course_router

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
app.include_router(router=auth_router)
app.include_router(router=course_router, prefix='/course')
app.include_router(router=main_router, tags=['main'])

app.include_router(router=api_auth_router, prefix='/api/auth', tags=['users'])
app.include_router(router=api_course_router, prefix='/api/course', tags=['course'])
