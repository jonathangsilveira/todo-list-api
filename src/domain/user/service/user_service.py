import logging
from typing import Optional

from src.domain.user.model.user_models import User, UserCreation, UserUpdate
from src.domain.user.repository.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def new_user(self, new_user: UserCreation) -> User:
        return await self._user_repository.insert_user(new_user)

    async def update_user(self, user_update: UserUpdate) -> User:
        return await self._user_repository.set_user(user_update)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self._user_repository.get_user_by_email_or_none(email)

    async def clear_users(self):
        return await self._user_repository.delete_all_users()