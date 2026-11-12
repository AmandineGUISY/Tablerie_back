from contextlib import asynccontextmanager
from db.database import create_db_and_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Controller.homeController import router as home_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

def load_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Routers --- #

    app.include_router(home_router)

    # --------------- #

    return app