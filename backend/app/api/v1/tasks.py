"""Содержит обработчики маршрутов для работы с задачами."""

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db import get_session
from app.models import UserModel
from app.schemas import (
    TaskCreateSchema,
    TaskListResponseSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
)
from app.services import create_task, delete_task, get_user_tasks, update_task
from app.services.exceptions import (
    TaskCreateException,
    TaskDeleteException,
    TaskUpdateException,
)

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
    task_data: TaskCreateSchema = Body(..., description="Данные для создания задачи"),
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
    except TaskCreateException as ex:
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


# MARK: UPDATE
@router.patch(
    "/{task_id}",
    summary="Обновить задачу",
    status_code=status.HTTP_200_OK,
)
async def update_task_route(
    task_id: int = Path(..., gt=0, description="ID задачи"),
    task_data: TaskUpdateSchema = Body(..., description="Данные для обновления задачи"),
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponseSchema:
    """
    Обновляет задачу по идентификатору.

    Args:
        task_id: Идентификатор задачи
        task_data: Данные для обновления задачи
        session: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        Обновленная задача

    Raises:
        HTTPException: Если задача не найдена или произошла ошибка при обновлении
    """
    try:
        return await update_task(
            session=session,
            task_id=task_id,
            task_data=task_data,
            user_id=current_user.id,
        )
    except TaskUpdateException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.msg,
        ) from ex
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex


# MARK: DELETE
@router.delete(
    "/{task_id}",
    summary="Удалить задачу",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task_route(
    task_id: int = Path(..., gt=0, description="ID задачи"),
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    """
    Удаляет задачу по идентификатору.

    Args:
        task_id: Идентификатор задачи
        session: Сессия базы данных
        current_user: Текущий пользователь

    Raises:
        HTTPException: Если задача не найдена или произошла ошибка при удалении
    """
    try:
        await delete_task(
            session=session,
            task_id=task_id,
            user_id=current_user.id,
        )
    except TaskDeleteException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.msg,
        ) from ex
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex
