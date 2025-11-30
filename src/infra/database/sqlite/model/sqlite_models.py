import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from src.domain.tasks.model.todo_task_status import TodoTaskStatus
from src.infra.database.sqlite.model.base_model import BaseEntity


class UserEntity(BaseEntity):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, unique=False, nullable=False)
    last_update_at = Column(DateTime, unique=False, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    def __init__(self, id: str, full_name: str, email: str, password: str, created_at: datetime.datetime,
                 last_update_at: Optional[datetime.datetime] = None, active: bool = True):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.last_update_at = last_update_at
        self.active = active


class TodoTaskEntity(BaseEntity):
    __tablename__ = "todo_tasks"

    id = Column(String, primary_key=True, unique=True)
    title = Column(String(100), nullable=False)
    status = Column(String, nullable=False, default=TodoTaskStatus.PENDING.value)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=False)
    last_sync_at = Column(DateTime, unique=False, nullable=True)

    def __init__(self, id: str, title: str,
                 status: str, owner_id: str,
                 created_at: datetime.datetime, updated_at: datetime.datetime,
                 last_sync_at: Optional[datetime.datetime]):
        self.id = id
        self.title = title
        self.status = status
        self.owner_id = owner_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_sync_at = last_sync_at
