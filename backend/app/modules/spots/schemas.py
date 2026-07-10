from sqlmodel import SQLModel

class SpotBase(SQLModel):
    """Base Schema for Skate Spots"""
    name: str
    description: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
