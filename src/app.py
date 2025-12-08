from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.health import health
from src.api.auth.v1 import auth
from src.api.tasks.v1 import tasks
from src.infra.database.redis.client import create_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    redis_client = await create_redis_client()
    app.state.redis_client = redis_client
    yield
    await redis_client.aclose()


def create_fastapi_app() -> FastAPI:
    api_app = FastAPI(lifespan=lifespan)
    api_app.include_router(health.router)
    api_app.include_router(auth.router)
    api_app.include_router(tasks.router)
    return api_app

app = create_fastapi_app()