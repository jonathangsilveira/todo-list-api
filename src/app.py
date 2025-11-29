import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.health import health
from src.api.auth.v1 import auth
from src.api.tasks.v1 import tasks
from src.infra.database.sqlite.creation import create_database_if_not_exists, create_database_engine, init_database
from src.infra.database.sqlite.session.async_session_factory import AsyncSessionFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    create_database_if_not_exists()
    db_connection_url = os.getenv("LOCAL_DATABASE_URL", "")
    debug_mode = bool(os.getenv("DEBUG_MODE", False))
    async_engine = create_database_engine(connection_url=db_connection_url, echo=debug_mode)
    await init_database(async_engine)
    async_session_factory = AsyncSessionFactory(async_engine=async_engine)
    app.state.async_session_factory = async_session_factory
    yield
    await async_engine.dispose()


def create_fastapi_app() -> FastAPI:
    api_app = FastAPI(lifespan=lifespan)
    api_app.include_router(health.router)
    api_app.include_router(auth.router)
    api_app.include_router(tasks.router)
    return api_app

app = create_fastapi_app()