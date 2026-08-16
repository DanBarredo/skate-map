from typing import Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    status_code: int
    message: str | None = None
    errors: list[str] | None = None
    data: T | None = None
