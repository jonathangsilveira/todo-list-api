import uuid
from datetime import datetime, timezone
from typing import Optional

from src.core.exception.exceptions import NotFoundException
from src.domain.user.exception.user_not_found import UserNotFoundException
from src.domain.user.model.user_models import User, UserCreation, UserUpdate
from src.domain.user.repository.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    _users: dict[str, User] = {}

    async def insert_user(self, user_creation: UserCreation) -> User:
        user_id = self._generate_uuid()
        user = User(
            id=user_id,
            full_name=user_creation.full_name,
            email=user_creation.email,
            password=user_creation.password,
            created_at=datetime.now(tz=timezone.utc),
            is_active=user_creation.is_active
        )
        self._users[user_creation.email] = user
        return user

    async def set_user(self, user_update: UserUpdate) -> User:
        user = self._users.get(user_update.email)
        if not user:
            raise NotFoundException(message=f"User ID {user_update.id} not found!")
        user.full_name = user_update.full_name
        user.password = user_update.password
        user.is_active = user_update.is_active
        user.last_update_at = datetime.now(tz=timezone.utc)
        return user

    async def get_user_by_email_or_none(self, email: str) -> Optional[User]:
        return self._users.get(email)

    async def delete_all_users(self) -> None:
        self._users.clear()

    @staticmethod
    def _generate_uuid() -> str:
        return str(uuid.uuid4())