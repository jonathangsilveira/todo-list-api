import uuid
from typing import Optional

from src.domain.user.model.new_user import NewUser
from src.domain.user.model.user import User
from src.domain.user.repository.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    _users: dict[str, User] = {}

    async def insert_user(self, user: NewUser) -> None:
        user_id = self._generate_uuid()
        self._users[user.email] = User(
            uuid=user_id,
            full_name=user.full_name,
            email=user.email,
            password=user.password
        )

    async def get_user_by_email_or_none(self, email: str) -> Optional[User]:
        return self._users[email]

    async def delete_all_users(self) -> None:
        self._users.clear()

    @staticmethod
    def _generate_uuid() -> str:
        return str(uuid.uuid4())