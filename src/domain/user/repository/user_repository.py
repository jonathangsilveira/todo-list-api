from abc import ABC, abstractmethod
from typing import Optional

from src.domain.user.model.user_models import User, UserCreation, UserUpdate


class UserRepository(ABC):

    @abstractmethod
    async def insert_user(self, user_creation: UserCreation) -> User:
        ...

    @abstractmethod
    async def set_user(self, user_update: UserUpdate) -> User:
        ...

    @abstractmethod
    async def get_user_by_email_or_none(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def delete_all_users(self) -> None:
        ...
