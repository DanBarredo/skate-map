from sqlmodel import SQLModel

class FavouriteBase(SQLModel):
    """Base Schema for User Favourites"""
    user_id: int
    spot_id: int
