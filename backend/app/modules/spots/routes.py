from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Placeholder spots route")
async def list_spots():
    return {"message": "Spots router placeholder"}
