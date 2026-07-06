from sqlmodel import SQLModel
from pydantic import EmailStr
import datetime

class UserCreate(SQLModel):
    """Schema for creating a new user"""
    username: str
    email: EmailStr
    password: str

class UserRead(SQLModel):
    """Schema for reading user data"""
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime