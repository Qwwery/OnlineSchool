from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web import user_router, auth_router, course_router, main_router
from app.api import api_auth_router, api_course_router, api_video_router, api_enroll_router

from app.models.db_session import global_init, create_session
from app.models import SqlAlchemyBase
from app.models.__all_models import *  # noqa: F401,F403 — регистрируем все модели
from app.crud import purge_expired_sessions
from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
db_patch = os.getenv('DATABASE_URL')
global_init(db_patch)

os.path.dirname(db_patch)

app = FastAPI()


@app.on_event('startup')
def on_startup():
    db = create_session()
    try:
        # Создаём отсутствующие таблицы (например, sessions.expires_at для новых БД)
        SqlAlchemyBase.metadata.create_all(db.bind)
        # Удаляем из базы сессии, у которых вышло время окончания
        purge_expired_sessions(db)
    finally:
        db.close()
app.mount(
    '/static',
    StaticFiles(directory=BASE_DIR / 'app' / 'static'),
    name='static'
)
app.include_router(router=user_router, tags=['users'])
app.include_router(router=auth_router, tags=['auth'])
app.include_router(router=course_router, prefix='/course', tags=['course'])
app.include_router(router=main_router, tags=['main'])

app.include_router(router=api_auth_router, prefix='/api/auth', tags=['auth'])
app.include_router(router=api_course_router, prefix='/api/course', tags=['course'])
app.include_router(router=api_video_router, prefix='/api/video', tags=['video'])
app.include_router(router=api_enroll_router, prefix='/api/enroll', tags=['enroll'])