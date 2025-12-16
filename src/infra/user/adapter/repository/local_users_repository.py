import traceback
import uuid
from datetime import datetime, timezone
from sqlite3 import IntegrityError
from typing import Optional

from sqlalchemy.future import select

from src.core.exception.exceptions import InternalErrorException, NotFoundException, ConflictException
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
        except Exception as exc:
            raise InternalErrorException(message="Error fetching user by e-mail") from exc

    async def insert_user(self, user_creation: UserCreation) -> User:
        try:
            generated_id = str(uuid.uuid4())
            user_entity = EntityUserMapper.new_user(generated_id, user_creation)

            async for session in self._async_session_factory.generate_session():
                try:
                    session.add(user_entity)
                except IntegrityError as exc:
                    raise ConflictException(message=f"User with e-mail {user_creation.email} already exists!") from exc

            return EntityUserMapper.from_entity(user_entity)
        except ConflictException:
            raise
        except Exception as exc:
            raise InternalErrorException(message=f"Error adding user {user_creation.full_name}") from exc

    async def set_user(self, user_update: UserUpdate) -> User:
        try:
            async for session in self._async_session_factory.generate_session():
                user_entity = await session.get(UserEntity, user_update.id)

                if not user_entity:
                    raise NotFoundException(message=f"User ID {user_update.id} not found!")

                user_entity.full_name = user_update.full_name
                user_entity.password = user_update.password
                user_entity.active = user_update.is_active
                user_entity.last_update_at = datetime.now(tz=timezone.utc)

            return EntityUserMapper.from_entity(user_entity)
        except NotFoundException:
            raise
        except Exception as exc:
            raise InternalErrorException(message=f"Error updating user {user_update.full_name}") from exc

    async def delete_all_users(self) -> None:
        try:
            async for session in self._async_session_factory.generate_session():
                statement = select(UserEntity)
                results = await session.execute(statement)
                all_users = results.scalars().all()

                for user in all_users:
                    await session.delete(user)
        except Exception as exc:
            raise InternalErrorException(message=f"Error removing all users") from exc