from sqlmodel import SQLModel

class SpotBase(SQLModel):
    """Base Schema for Skate Spots"""
    name: str
    description: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class SpotCreate(SpotBase):
    """Schema for creating a new skate spot"""
    pass

class SpotRead(SpotBase):
    """Schema for reading skate spot data"""
    id: int

class SpotUpdate(SpotBase):
    """Schema for updating skate spot data"""
    pass
