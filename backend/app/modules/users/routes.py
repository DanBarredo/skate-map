from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.modules.users.models import User
from app.modules.users.schemas import UserRead
