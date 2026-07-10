from sqlmodel import SQLModel, Field
import datetime

class Spot(SQLModel, table=True):
    """Database Table for Skate Spots"""
    __tablename__: str = "spots" # type: ignore

    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    description: str | None = Field(default=None)
    location: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
