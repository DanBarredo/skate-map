from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from .models import Spot
from .schemas import SpotCreate, SpotRead, SpotUpdate


# TODO: review CRUD logic and add error handling etc
class SpotService:
    """Service layer for spot CRUD operations."""

    def __init__(self, session: Session):
        self.session = session

    def list_spots(self) -> list[SpotRead]:
        """Return all spots as response DTOs."""
        statement = select(Spot)
        spots = self.session.exec(statement).all()
        return [SpotRead.model_validate(spot) for spot in spots]

    def get_spot(self, spot_id: int) -> SpotRead | None:
        """Return a single spot by ID."""
        statement = select(Spot).where(Spot.id == spot_id)
        spot = self.session.exec(statement).first()
        if spot is None:
            return None
        return SpotRead.model_validate(spot)

    def create_spot(self, dto: SpotCreate) -> SpotRead:
        """Create a new spot and return its read representation."""
        spot = Spot(**dto.model_dump())
        try:
            self.session.add(spot)
            self.session.commit()
            self.session.refresh(spot)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("A spot with that name already exists.")

        return SpotRead.model_validate(spot)

    def update_spot(self, spot_id: int, dto: SpotUpdate) -> SpotRead | None:
        """Update an existing spot by ID."""
        statement = select(Spot).where(Spot.id == spot_id)
        spot = self.session.exec(statement).first()
        if spot is None:
            return None

        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(spot, field, value)

        try:
            self.session.add(spot)
            self.session.commit()
            self.session.refresh(spot)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("A spot with that name already exists.")

        return SpotRead.model_validate(spot)

    def delete_spot(self, spot_id: int) -> bool:
        """Delete a spot by ID and return whether it existed."""
        statement = select(Spot).where(Spot.id == spot_id)
        spot = self.session.exec(statement).first()
        if spot is None:
            return False

        self.session.delete(spot)
        self.session.commit()
        return True
