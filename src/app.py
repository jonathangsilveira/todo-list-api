from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.health import health
from src.api.auth.v1 import auth
from src.api.tasks.v1 import tasks


def create_fastapi_app() -> FastAPI:
    load_dotenv()
    api_app = FastAPI()
    api_app.include_router(health.router)
    api_app.include_router(auth.router)
    api_app.include_router(tasks.router)
    return api_app

app = create_fastapi_app()