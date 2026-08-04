from fastapi import APIRouter

# TODO: wire new service into routes

router = APIRouter()

@router.get("/", summary="Placeholder spots route")
async def list_spots():
    return {"message": "Spots router placeholder"}

@router.post("/", summary="Placeholder create spot route")
async def create_spot():
    return {"message": "Spot created successfully"}

@router.put("/{spot_id}", summary="Placeholder update spot route")
async def update_spot(spot_id: int):
    return {"message": f"Spot with ID {spot_id} updated successfully"}
