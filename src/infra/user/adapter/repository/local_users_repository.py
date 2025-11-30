import traceback
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.future import select

from src.domain.user.exception.user_not_found import UserNotFoundException
from src.domain.user.model.user_models import UserCreation, User, UserUpdate
from src.domain.user.repository.user_repository import UserRepository
from src.infra.database.exception.exceptions import DatabaseWriteException, DatabaseReadException
from src.infra.database.sqlite.model.sqlite_models import UserEntity
from src.infra.database.sqlite.session.async_session_factory import AsyncSessionFactory
from src.infra.user.mapper.entity_user_mapper import EntityUserMapper


class LocalUsersRepository(UserRepository):

    def __init__(self, async_session_factory: AsyncSessionFactory):
        self._async_session_factory = async_session_factory

    async def get_user_by_email_or_none(self, email: str) -> Optional[User]:
        try:
            statement = select(UserEntity).where(email == UserEntity.email)
            async for session in self._async_session_factory.generate_session():
                results = await session.execute(statement)
                user_entity = results.scalars().first()
                return EntityUserMapper.from_entity(user_entity) if user_entity else None
        except Exception:
            details = traceback.format_exc()
            raise DatabaseReadException(details=details)

    async def insert_user(self, user_creation: UserCreation) -> User:
        try:
            generated_id = str(uuid.uuid4())
            user_entity = EntityUserMapper.new_user(generated_id, user_creation)

            async for session in self._async_session_factory.generate_session():
                session.add(user_entity)

            return EntityUserMapper.from_entity(user_entity)
        except Exception:
            details = traceback.format_exc()
            raise DatabaseWriteException(details=details)

    async def set_user(self, user_update: UserUpdate) -> User:
        async for session in self._async_session_factory.generate_session():
            try:
                user_entity: Optional[type[UserEntity]] = await session.get(UserEntity, user_update.id)
            except Exception:
                details = traceback.format_exc()
                raise DatabaseReadException(details=details)

            if not user_entity:
                raise UserNotFoundException()

            try:
                user_entity.full_name = user_update.full_name
                user_entity.password = user_update.password
                user_entity.active = user_update.is_active
                user_entity.last_update_at = datetime.now(tz=timezone.utc)
            except Exception:
                details = traceback.format_exc()
                raise DatabaseWriteException(details=details)

            return EntityUserMapper.from_entity(user_entity)

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
