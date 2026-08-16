from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_db
from app.modules.users.schemas import UserCreate, UserRead
from app.modules.users.services import UserService
from app.utils.api_response import ApiResponse

router = APIRouter()


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session=session)


@router.post(
    "/",
    summary="Create a new user",
    response_model=ApiResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    dto: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.create_user(dto=dto)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to create user.",
            )
        return ApiResponse(
            status_code=status.HTTP_201_CREATED,
            message="User created successfully.",
            data=UserRead.model_validate(user),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{user_id}",
    summary="Get a user by ID",
    response_model=ApiResponse[UserRead],
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user_details(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully.",
        data=user,
    )


@router.put(
    "/{user_id}/username",
    summary="Update a user's username",
    response_model=ApiResponse[UserRead],
)
async def update_username(
    user_id: int,
    new_username: str,
    service: UserService = Depends(get_user_service),
):
    user = service.update_username(user_id=user_id, new_username=new_username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="Username updated successfully.",
        data=user,
    )
