from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug
)

SessionLocal = Session

def init_db():
    SQLModel.metadata.create_all(bind=engine)

def get_db():
    with SessionLocal(engine) as session:
        yield session
