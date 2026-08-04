from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Placeholder favourites route")
async def list_favourites():
    return {"message": "Favourites router placeholder"}
