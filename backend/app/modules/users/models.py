from sqlmodel import SQLModel, Field
from pydantic import EmailStr
import datetime

class User(SQLModel, table=True, table_name="users"):
    """Database Table for Users"""
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
