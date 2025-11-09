from abc import ABC, abstractmethod
from typing import Optional

from src.domain.user.model.new_user import NewUser
from src.domain.user.model.user import User


class UserRepository(ABC):

    @abstractmethod
    async def insert_user(self, user: NewUser) -> None:
        ...

    @abstractmethod
    async def get_user_by_email_or_none(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def delete_all_users(self) -> None:
        ...