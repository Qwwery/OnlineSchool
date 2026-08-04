from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.web.pages import router
from app.models.db_session import global_init
from pathlib import Path
import dotenv
import os
import pretty_errors

dotenv.load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
db_patch = os.getenv('db_patch')
global_init(db_patch)

os.path.dirname(db_patch, exist_ok=True)

app = FastAPI()
app.mount(
    '/static',
    StaticFiles(directory=BASE_DIR / 'app' / 'static'),
    name='static'
)
app.include_router(router=router)
