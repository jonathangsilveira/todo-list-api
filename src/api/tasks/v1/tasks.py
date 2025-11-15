from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from starlette import status

from src.api.auth.dependencies import get_authorized_user
from src.api.tasks.dependencies import get_todo_tasks_service
from src.api.tasks.request.new_todo_task_input import NewTodoTaskInput
from src.api.tasks.response.task import TasksResponse, TaskResponse
from src.domain.tasks.exception.todo_task_already_exists import TodoTaskAlreadyExistsException
from src.domain.tasks.exception.todo_task_change import TodoTaskChangeException
from src.domain.tasks.exception.todo_task_fetch import TodoTaskFetchException
from src.domain.tasks.exception.todo_task_not_found import TodoTaskNotFoundException
from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.domain.user.model.user import User

router = APIRouter(
    prefix="/tasks/v1",
    tags=["Tasks"],
    dependencies=[Depends(get_authorized_user)]
)


@router.get(path="/all", status_code=status.HTTP_200_OK, response_model=TasksResponse)
async def get_all_tasks(authorized_user: User = Depends(get_authorized_user),
                        todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        todo_tasks = await todo_tasks_service.get_todo_tasks_by_user(user_id=authorized_user.uuid)
        return TasksResponse(tasks=[TaskResponse.from_domain(task) for task in todo_tasks])
    except TodoTaskFetchException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error fetching tasks.")


@router.get(path="/task/{uuid}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def get_todo_task_by_uuid(todo_task_uuid: str = Path(alias="uuid"),
                                todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        todo_task = await todo_tasks_service.get_todo_task_by_uuid(uuid=todo_task_uuid)
        return TaskResponse.from_domain(todo_task)
    except TodoTaskNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo task {todo_task_uuid} not found.")
    except TodoTaskFetchException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error fetching todo task: {todo_task_uuid}")


@router.post(path="/task/new", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def add_todo_task(new_todo_task_input: NewTodoTaskInput,
                        authorized_user: User = Depends(get_authorized_user),
                        todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        new_todo_task = new_todo_task_input.to_domain()
        created_task = await todo_tasks_service.add_todo_task(user_id=authorized_user.uuid, todo_task=new_todo_task)
        return TaskResponse.from_domain(created_task)
    except TodoTaskAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Todo task {new_todo_task_input.uuid} already exists.")
    except TodoTaskChangeException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error creating task.")

@router.patch(path="/task/{uuid}/done", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def mark_todo_task_as_done(todo_task_uuid: str = Path(alias="uuid"),
                                 todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        updated_task = await todo_tasks_service.mark_todo_task_as_done(uuid=todo_task_uuid)
        return TaskResponse.from_domain(updated_task)
    except TodoTaskNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo task {todo_task_uuid} not found.")
    except TodoTaskChangeException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error updating todo task: {todo_task_uuid}")


@router.delete(path="/task/{uuid}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo_task(todo_task_uuid: str = Path(alias="uuid"),
                           todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        await todo_tasks_service.remove_todo_task_by_uuid(uuid=todo_task_uuid)
    except TodoTaskNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo task {todo_task_uuid} not found.")