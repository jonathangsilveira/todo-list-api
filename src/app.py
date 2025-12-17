from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.auth.v1 import auth
from src.api.health import health
from src.api.tasks.v1 import tasks
from src.dependency_injection.dependency_container import DependencyContainer
from src.infra.database.sqlite.creation import create_database_if_not_exists, init_database
from src.infra.exception_handlers.fastapi_exception_handler import setup_exception_handling


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    container = DependencyContainer()
    container.init_resources()
    create_database_if_not_exists()
    async_engine = container.async_engine()
    await init_database(async_engine)
    redis_client = container.redis_client()
    yield
    await redis_client.aclose()
    await async_engine.dispose()
    container.shutdown_resources()


def create_fastapi_app() -> FastAPI:
    api_app = FastAPI(lifespan=lifespan)

    setup_exception_handling(api_app)

    api_app.include_router(health.router)
    api_app.include_router(auth.router)
    api_app.include_router(tasks.router)
    return api_app

app = create_fastapi_app()