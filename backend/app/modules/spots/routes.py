from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.utils.api_response import ApiResponse
from app.database import get_db
from app.modules.spots.schemas import SpotCreate, SpotRead, SpotUpdate
from app.modules.spots.services import SpotService

router = APIRouter()


def get_spot_service(session: Session = Depends(get_db)) -> SpotService:
    return SpotService(session=session)


@router.get("/", summary="List skate spots", response_model=ApiResponse[list[SpotRead]])
async def list_spots(
    service: SpotService = Depends(get_spot_service),
):
    spots = service.list_spots()
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="Spots retrieved successfully.",
        data=spots,
    )


@router.get(
    "/{spot_id}",
    summary="Get a skate spot by ID",
    response_model=ApiResponse[SpotRead],
)
async def get_spot(
    spot_id: int,
    service: SpotService = Depends(get_spot_service),
):
    spot = service.get_spot(spot_id=spot_id)
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spot not found.",
        )
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="Spot retrieved successfully.",
        data=spot,
    )


@router.post(
    "/",
    summary="Create a new skate spot",
    response_model=ApiResponse[SpotRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_spot(
    dto: SpotCreate,
    service: SpotService = Depends(get_spot_service),
):
    try:
        spot = service.create_spot(dto=dto)
        return ApiResponse(
            status_code=status.HTTP_201_CREATED,
            message="Spot created successfully.",
            data=spot,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/{spot_id}",
    summary="Update a skate spot",
    response_model=ApiResponse[SpotRead],
)
async def update_spot(
    spot_id: int,
    dto: SpotUpdate,
    service: SpotService = Depends(get_spot_service),
):
    try:
        updated_spot = service.update_spot(spot_id=spot_id, dto=dto)
        if updated_spot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Spot not found.",
            )
        return ApiResponse(
            status_code=status.HTTP_200_OK,
            message="Spot updated successfully.",
            data=updated_spot,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{spot_id}",
    summary="Delete a skate spot",
    response_model=ApiResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_spot(
    spot_id: int,
    service: SpotService = Depends(get_spot_service),
):
    deleted_id = spot_id
    deleted = service.delete_spot(spot_id=spot_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spot not found.",
        )
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="Spot deleted successfully.",
        data= {"id": deleted_id},
    )
