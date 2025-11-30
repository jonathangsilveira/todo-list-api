import traceback
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.future import select

from src.domain.tasks.exception.todo_task_not_found import TodoTaskNotFoundException
from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask
from src.domain.tasks.model.todo_task_status import TodoTaskStatus
from src.domain.tasks.repository.todo_tasks_repository import TodoTasksRepository
from src.infra.database.exception.exceptions import DatabaseReadException, DatabaseWriteException
from src.infra.database.sqlite.model.sqlite_models import TodoTaskEntity
from src.infra.database.sqlite.session.async_session_factory import AsyncSessionFactory
from src.infra.tasks.mapper.entity_todo_task_mapper import EntityTodoTaskMapper


class LocalTodoTasksRepository(TodoTasksRepository):

    def __init__(self, _async_session_generator: AsyncSessionFactory):
        self._async_session_generator = _async_session_generator

    async def get_todo_tasks_by_user(self, user_id: str) -> list[TodoTask]:
        try:
            async for session in self._async_session_generator.generate_session():
                statement = select(TodoTaskEntity).where(user_id == TodoTaskEntity.owner_id)
                results = await session.execute(statement)
                todo_task_entity = results.scalars().all()
                return [EntityTodoTaskMapper.from_entity(entity) for entity in todo_task_entity]
        except Exception:
            details = traceback.format_exc()
            raise DatabaseReadException(details=details)
        return []

    async def get_todo_task_by_uuid(self, uuid: str) -> Optional[TodoTask]:
        try:
            async for session in self._async_session_generator.generate_session():
                todo_task_entity = await session.get(TodoTaskEntity, uuid)

                return EntityTodoTaskMapper.from_entity(todo_task_entity) if todo_task_entity else None

            return None
        except Exception:
            details = traceback.format_exc()
            raise DatabaseReadException(details=details)

    async def add_todo_task(self, user_id: str, todo_task: NewTodoTask) -> TodoTask:
        try:
            todo_task_entity = EntityTodoTaskMapper.new_entity(todo_task, user_id)

            async for session in self._async_session_generator.generate_session():
                session.add(todo_task_entity)

            return EntityTodoTaskMapper.from_entity(todo_task_entity)
        except Exception:
            details = traceback.format_exc()
            raise DatabaseWriteException(details=details)

    async def mark_todo_task_as_done(self, uuid: str) -> TodoTask:
        try:
            async for session in self._async_session_generator.generate_session():
                todo_task_entity = await session.get(TodoTaskEntity, uuid)

                if not todo_task_entity:
                    raise TodoTaskNotFoundException()

                todo_task_entity.status = TodoTaskStatus.DONE.value()
                todo_task_entity.updated_at = datetime.now(tz=timezone.utc)
                todo_task_entity.last_sync_at = datetime.now(tz=timezone.utc)

            return EntityTodoTaskMapper.from_entity(todo_task_entity)
        except Exception:
            details = traceback.format_exc()
            raise DatabaseWriteException(details=details)

    async def remove_todo_task_by_uuid(self, uuid: str) -> None:
        try:
            async for session in self._async_session_generator.generate_session():
                todo_task_entity = await session.get(TodoTaskEntity, uuid)

                if not todo_task_entity:
                    raise TodoTaskNotFoundException()

                await session.delete(todo_task_entity)
        except Exception:
            details = traceback.format_exc()
            raise DatabaseWriteException(details=details)