import traceback
from typing import Optional

from sqlalchemy.future import select

from src.domain.user.model.new_user import NewUser
from src.domain.user.model.user import User
from src.domain.user.repository.user_repository import UserRepository
from src.infra.database.exception.exceptions import DatabaseWriteException, DatabaseReadException
from src.infra.database.sqlite.model.sqlite_models import UserEntity
from src.infra.database.sqlite.session.async_session_factory import AsyncSessionFactory


class LocalUsersRepository(UserRepository):

    def __init__(self, async_session_factory: AsyncSessionFactory):
        self._async_session_factory = async_session_factory

    async def insert_user(self, user: NewUser) -> None:
        try:
            entity = UserEntity(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                password=user.password,
                active=user.is_active
            )
            async for session in self._async_session_factory.generate_session():
                session.add(entity)
        except Exception:
            details = traceback.format_exc()
            raise DatabaseWriteException(details=details)

    async def get_user_by_email_or_none(self, email: str) -> Optional[User]:
        try:
            statement = select(UserEntity).where(email == UserEntity.email)
            async for session in self._async_session_factory.generate_session():
                results = await session.execute(statement)
                user_entity = results.scalars().first()
                return User(
                    uuid=user_entity.id,
                    full_name=user_entity.full_name,
                    email=user_entity.email,
                    password=user_entity.password,
                    is_active=user_entity.active
                ) if user_entity else None
        except Exception:
            details = traceback.format_exc()
            raise DatabaseReadException(details=details)

    async def delete_all_users(self) -> None:
        async for session in self._async_session_factory.generate_session():
            try:
                statement = select(UserEntity)
                results = await session.execute(statement)
                all_users = results.scalars().all()
            except Exception:
                details = traceback.format_exc()
                raise DatabaseReadException(details=details)
            try:
                for user in all_users:
                    await session.delete(user)
            except Exception:
                details = traceback.format_exc()
                raise DatabaseWriteException(details=details)
