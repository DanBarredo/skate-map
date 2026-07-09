from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Initialize the database on startup
        init_db()
        yield

    app = FastAPI(title="Skate Map", debug=settings.debug, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    try:
        # Include routers for spots module
        from app.modules.spots.routes import router as spots_router
        app.include_router(spots_router, prefix="/spots", tags=["Spots"])
    except Exception:
        pass

    try:
        # Include routes for users module
        from app.modules.users.routes import router as users_router
        app.include_router(users_router, prefix="/users", tags=["Users"])
    except Exception:
        pass

    try:
        # Include routes for favourites module
        from app.modules.favourites.routes import router as favourites_router
        app.include_router(favourites_router, prefix="/favourites", tags=["Favourites"])
    except Exception:
        pass

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000, reload=True)

