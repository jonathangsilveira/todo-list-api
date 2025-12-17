import os

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy_utils import database_exists, create_database

from src.infra.database.sqlite.model.base_model import BaseEntity


def create_database_if_not_exists():
    db_path = "db"
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    connection_url = "sqlite:///db/todo_list.sqlite3"
    if not database_exists(connection_url):
        create_database(connection_url)

def create_database_engine(connection_url: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(
        url=connection_url,
        echo=echo
    )

async def init_database(async_engine: AsyncEngine):
    async with async_engine.begin() as connection:
        await connection.run_sync(fn=BaseEntity.metadata.create_all)