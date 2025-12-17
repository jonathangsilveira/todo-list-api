import logging
from typing import Optional

from src.core.exception.exceptions import ConflictException, InternalErrorException, NotFoundException
from src.domain.user.model.user_models import User, UserCreation, UserUpdate
from src.domain.user.repository.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def new_user(self, user_creation: UserCreation) -> User:
        try:
            logger.info(f"Creating new user {user_creation.email}...")
            return await self._user_repository.insert_user(user_creation)
        except ConflictException as exc:
            logger.error(msg=exc.message, exc_info=exc)
            raise exc
        except InternalErrorException as exc:
            logger.error(msg=f"Error creating new user: {user_creation.email}", exc_info=exc)
            raise exc

    async def update_user(self, user_update: UserUpdate) -> User:
        try:
            logger.info(f"Updating user {user_update.email}...")
            return await self._user_repository.set_user(user_update)
        except InternalErrorException as exc:
            logger.error(msg=f"Error updating user: {user_update.email}", exc_info=exc)
            raise exc

    async def get_user_by_email(self, email: str) -> User:
        try:
            logger.info(msg=f"Fetching user by e-mail: {email}")
            user = await self._user_repository.get_user_by_email_or_none(email)

            if not user:
                raise NotFoundException(message=f"User with email {email} was not found.")

            return user
        except NotFoundException as exc:
            logger.error(msg=f"User with email {email} was not found.", exc_info=exc)
            raise exc
        except InternalErrorException as exc:
            logger.error(msg=f"Error fetching user by e-mail: {email}", exc_info=exc)
            raise exc

    async def clear_users(self):
        try:
            logger.info(msg=f"Clearing users from database...")
            await self._user_repository.delete_all_users()
        except InternalErrorException as exc:
            logger.error(msg=f"Error removing all users", exc_info=exc)
            raise exc