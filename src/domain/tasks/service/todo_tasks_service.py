import logging

from src.core.exception.exceptions import NotFoundException, InternalErrorException
from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask
from src.domain.tasks.repository.todo_tasks_repository import TodoTasksRepository

logger = logging.getLogger(__name__)


class TodoTasksService:

    def __init__(self, todo_tasks_repository: TodoTasksRepository) -> None:
        self._todo_tasks_repository = todo_tasks_repository

    async def get_todo_tasks_by_user(self, user_id: str) -> list[TodoTask]:
        logger.info(msg=f"Fetching TODO tasks by user id: {user_id}")
        try:
            return await self._todo_tasks_repository.get_todo_tasks_by_user(user_id)
        except InternalErrorException as exc:
            logger.error(msg=f"Error fetching TODO task by user: {user_id}", exc_info=exc)
            raise exc

    async def get_todo_task_by_uuid(self, uuid: str) -> TodoTask:
        logger.info(msg=f"Fetch TODO tasks by uuid: {uuid}")
        try:
            todo_task = await self._todo_tasks_repository.get_todo_task_by_uuid(uuid)

            if not todo_task:
                logger.error(msg=f"TODO task {uuid} not found!")
                raise NotFoundException(message=f"TODO task {uuid} not found!")

            return todo_task
        except InternalErrorException as exc:
            logger.error(msg=f"Error fetching TODO task by uuid {uuid}", exc_info=exc)
            raise exc

    async def upsert_todo_task(self, user_id: str, todo_task: NewTodoTask) -> TodoTask:
        logger.info(msg=f"Upserting TODO task {todo_task.uuid} for user {user_id}...")
        try:
            return await self._todo_tasks_repository.upsert_todo_task(user_id, todo_task)
        except InternalErrorException as exc:
            logger.error(msg=f"Error upserting TODO task {todo_task.uuid}", exc_info=exc)
            raise exc

    async def mark_todo_task_as_done(self, uuid: str) -> TodoTask:
        try:
            return await self._todo_tasks_repository.mark_todo_task_as_done(uuid)
        except InternalErrorException as exc:
            logger.error(msg=f"Error updating TODO task to DONE by uuid: {uuid}", exc_info=exc)
            raise exc

    async def remove_todo_task_by_uuid(self, uuid: str) -> None:
        try:
            await self._todo_tasks_repository.remove_todo_task_by_uuid(uuid)
        except InternalErrorException as exc:
            logger.error(msg=f"Error removing TODO task by uuid: {uuid}", exc_info=exc)
            raise exc
