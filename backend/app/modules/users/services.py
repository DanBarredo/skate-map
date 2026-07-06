from pwdlib import PasswordHash

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from .models import User
from .schemas import UserCreate, UserRead

_pwd = PasswordHash.recommended()

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, dto: UserCreate) -> User|None:
        """Create a new user in the database."""
        # Check if a user with the same email or username already exists
        exists = self.session.exec(select(User).where(User.email == dto.email)).first()
        if exists:
            raise ValueError("User with this email already exists.")
        duplicate_username = self.session.exec(select(User).where(User.username == dto.username)).first()
        if duplicate_username:
            raise ValueError("Username already exists.")

        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=_pwd.hash(password=dto.password)
        )
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Failed to create user due to database integrity error.")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return _pwd.verify(password=plain_password, hash=hashed_password)
    
    def get_user_details(self, user_id: int) -> UserRead|None:
        """Retrieve user details by user ID."""
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).first()
        if not user:
            return None
        return UserRead.model_validate(user)
    
    def update_username(self, user_id: int, new_username:str) -> UserRead|None:
        """Update the username of a user."""
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).first()
        if not user:
            return None
        user.username = new_username
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return UserRead.model_validate(user)
    