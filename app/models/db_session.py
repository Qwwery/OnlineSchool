from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy import create_engine

SqlAlchemyBase = declarative_base()
__factory = None

def global_init(db_file: str):
    global __factory
    if __factory:
        return __factory

    if not db_file or not db_file.strip():
        raise Exception("Нет файла")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from . import __all_models 

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()

def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()