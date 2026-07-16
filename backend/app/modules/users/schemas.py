from sqlmodel import SQLModel
from pydantic import EmailStr
import datetime

class UserCreate(SQLModel):
    """Schema for creating a new user"""
    username: str
    email: EmailStr
    password: str

class UserRead(SQLModel):
    """Schema for reading user data. Use also for UserResponse for createUser API"""
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime

class UserUpdate(SQLModel):
    """Schema for updating user data"""
    username: str | None = None
    password: str | None = None