from datetime import datetime, timezone

from src.domain.user.model.user_models import UserCreation, UserUpdate, User
from src.infra.database.sqlite.model.sqlite_models import UserEntity


class EntityUserMapper:

    @staticmethod
    def new_user(generated_id: str, user_creation: UserCreation) -> UserEntity:
        return UserEntity(
            id=generated_id,
            full_name=user_creation.full_name,
            email=user_creation.email,
            password=user_creation.password,
            active=user_creation.is_active,
            created_at=datetime.now(tz=timezone.utc)
        )

    @staticmethod
    def to_entity(user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            password=user.password,
            active=user.is_active,
            created_at=user.created_at,
            last_update_at=user.last_update_at
        )

    @staticmethod
    def from_entity(user_entity: UserEntity) -> User:
        return User(
            id=user_entity.id,
            full_name=user_entity.full_name,
            email=user_entity.email,
            password=user_entity.password,
            is_active=user_entity.is_active,
            created_at=user_entity.created_at,
            last_update_at=user_entity.last_update_at
        )