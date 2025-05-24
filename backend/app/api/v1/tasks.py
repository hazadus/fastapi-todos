from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db import get_session
from app.models import UserModel
from app.schemas import TaskCreateSchema, TaskListResponseSchema, TaskResponseSchema
from app.services import create_task, get_user_tasks
from app.services.exceptions import TaskCreationException

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)


# MARK: POST
@router.post(
    "",
    summary="Создать новую задачу",
    status_code=status.HTTP_201_CREATED,
)
async def create_task_route(
    task_data: TaskCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponseSchema:
    """
    Создает новую задачу для текущего пользователя.

    Args:
        task_data: Данные для создания задачи
        session: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        TaskResponseSchema: Созданная задача
    """
    try:
        return await create_task(
            session=session,
            task_data=task_data,
            user_id=current_user.id,
        )
    except TaskCreationException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.msg,
        ) from ex
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex


# MARK: GET
@router.get(
    "",
    summary="Получить все задачи текущего пользователя",
    status_code=status.HTTP_200_OK,
)
async def get_user_tasks_route(
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> TaskListResponseSchema:
    """
    Получает все задачи текущего пользователя.

    Args:
        session: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        Список задач текущего пользователя
    """
    try:
        tasks = await get_user_tasks(
            session=session,
            user_id=current_user.id,
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex

    return TaskListResponseSchema(
        tasks=tasks,
        total=len(tasks),
    )
