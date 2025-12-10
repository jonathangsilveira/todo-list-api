from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.auth.v1 import auth
from src.api.health import health
from src.api.tasks.v1 import tasks
from src.dependency_injection.dependency_container import DependencyContainer


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    container = DependencyContainer()
    container.init_resources()
    redis_client = container.redis_client()
    yield
    await redis_client.aclose()
    container.shutdown_resources()


def create_fastapi_app() -> FastAPI:
    api_app = FastAPI(lifespan=lifespan)
    api_app.include_router(health.router)
    api_app.include_router(auth.router)
    api_app.include_router(tasks.router)
    return api_app

app = create_fastapi_app()