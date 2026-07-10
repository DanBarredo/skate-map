from sqlmodel import Relationship, SQLModel, Field
from pydantic import EmailStr
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.favourites.models import Favourite

class User(SQLModel, table=True, table_name="users"):
    """Database Table for Users"""
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )

    favourites: list["Favourite"] = Relationship(back_populates="user")
