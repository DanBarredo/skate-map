from sqlmodel import SQLModel
from app.modules.spots.schemas import SpotRead

class FavouriteBase(SQLModel):
    """Base Schema for User Favourites"""
    user_id: int
    spot_id: int

class FavouriteCreate(FavouriteBase):
    """Schema for creating a new favourite"""
    pass

class FavouriteResponse(FavouriteBase):
    """Schema for reading favourite data"""
    id: int
    spot: SpotRead | None = None
