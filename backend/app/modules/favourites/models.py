from sqlmodel import SQLModel, Field, Relationship
import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.spots.models import Spot

class Favourite(SQLModel, table=True, table_name="favourites"):
    """Database Table for User Favourites"""
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    spot_id: int = Field(default=None, foreign_key="spots.id")
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )

    # Relationships
    # TODO: link to User and Spot models
    user: Optional["User"] = Relationship(back_populates="favourites")
    spot: Optional["Spot"] = Relationship()
