from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio.session import AsyncSession


class AsyncSessionFactory:

    def __init__(self, async_engine: AsyncEngine):
        self._async_session_factory = async_sessionmaker[AsyncSession](
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    async def generate_session(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self._async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e