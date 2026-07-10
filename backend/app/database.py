from typing import Generator

from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

# import module models here
from app.modules.spots.models import Spot # noqa: F401
from app.modules.favourites.models import Favourite # noqa: F401
from app.modules.users.models import User # noqa: F401

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug
)

SessionLocal = Session

def init_db() -> None:
    """
    Create all tables defined by SQLModel models in the database.
    """
    SQLModel.metadata.create_all(bind=engine)
    print("Database initialized and tables created.")

def get_db() -> Generator[Session, None, None]:
    """
    Yield database session for dependency injection in FastAPI routes."""
    with SessionLocal(engine) as session:
        yield session
