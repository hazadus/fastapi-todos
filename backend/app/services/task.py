"""Содержит бизнес-логику для работы с задачами."""

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import TaskDAO
from app.schemas import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema
from app.services.exceptions import (
    TaskCreateException,
    TaskDeleteException,
    TaskNotFoundException,
    TaskUpdateException,
)


# MARK: Create
async def create_task(
    *,
    session: AsyncSession,
    task_data: TaskCreateSchema,
    user_id: int,
) -> TaskResponseSchema:
    """
    Создает новую задачу в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy
        task_data (TaskCreateSchema): Данные для создания задачи
        user_id (int): Идентификатор пользователя, создающего задачу
    Returns:
        Созданная задача
    Raises:
        TaskCreateException: Если задача не была создана
    """
    db_task = await TaskDAO.add(
        session=session,
        obj_in={
            **task_data.model_dump(exclude_unset=True),
            "user_id": user_id,
        },
    )
    if not db_task:
        raise TaskCreateException

    try:
        response_data = TaskResponseSchema.model_validate(db_task)
    except ValidationError as e:
        raise TaskCreateException from e

    await session.commit()
    return response_data


# MARK: Read
async def get_user_tasks(
    *,
    session: AsyncSession,
    user_id: int,
) -> list[TaskResponseSchema]:
    """
    Получает все задачи пользователя.

    Args:
        session: Асинхронная сессия SQLAlchemy
        user_id (int): Идентификатор пользователя
    Returns:
        Список задач пользователя
    """
    db_tasks = await TaskDAO.find_all(
        session=session,
        user_id=user_id,
    )

    if not db_tasks:
        return []

    return [TaskResponseSchema.model_validate(task) for task in db_tasks]


async def get_task_by_id(
    *,
    session: AsyncSession,
    task_id: int,
    user_id: int,
) -> TaskResponseSchema:
    """
    Получает задачу по идентификатору.

    Args:
        session: Асинхронная сессия SQLAlchemy
        task_id (int): Идентификатор задачи
        user_id (int): Идентификатор пользователя, которому принадлежит задача
    Returns:
        Задача с указанным идентификатором
    Raises:
        TaskNotFoundException: Если задача не найдена
    """
    # Проверяем, существует ли задача с указанным идентификатором и принадлежит ли
    # она пользователю
    db_task = await TaskDAO.find_one_or_none(
        session,
        TaskDAO.model.id == task_id,
        TaskDAO.model.user_id == user_id,
    )

    if not db_task:
        raise TaskNotFoundException

    try:
        return TaskResponseSchema.model_validate(db_task)
    except ValidationError as e:
        raise TaskNotFoundException from e


# MARK: Update
async def update_task(
    *,
    session: AsyncSession,
    task_id: int,
    task_data: TaskUpdateSchema,
    user_id: int,
) -> TaskResponseSchema:
    """
    Обновляет задачу в базе данных. Задача должна принадлежать
    пользователю с указанным user_id.

    Args:
        session: Асинхронная сессия SQLAlchemy
        task_id (int): Идентификатор задачи для обновления
        task_data (TaskUpdateSchema): Данные для обновления задачи
        user_id (int): Идентификатор пользователя, обновляющего задачу
    Returns:
        Обновленная задача
    Raises:
        TaskUpdateException: Если задача не была обновлена
    """
    # Проверяем, существует ли задача с указанным идентификатором и принадлежит ли
    # она пользователю
    db_task = await TaskDAO.update(
        session,
        TaskDAO.model.id == task_id,
        TaskDAO.model.user_id == user_id,
        obj_in=task_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        ),
    )

    if not db_task:
        raise TaskUpdateException

    try:
        response_data = TaskResponseSchema.model_validate(db_task)
    except ValidationError as e:
        raise TaskUpdateException from e

    await session.commit()
    return response_data


# MARK: Delete
async def delete_task(
    *,
    session: AsyncSession,
    task_id: int,
    user_id: int,
) -> None:
    """
    Удаляет задачу из базы данных. Задача должна принадлежать
    пользователю с указанным user_id.

    Args:
        session: Асинхронная сессия SQLAlchemy
        task_id (int): Идентификатор задачи для удаления
        user_id (int): Идентификатор пользователя, удаляющего задачу
    Raises:
        TaskDeleteException: Если задача не была удалена
    """
    # Проверяем, существует ли задача с указанным идентификатором и принадлежит ли
    # она пользователю
    row_count = await TaskDAO.delete(
        session,
        TaskDAO.model.id == task_id,
        TaskDAO.model.user_id == user_id,
    )

    if row_count != 1:
        raise TaskDeleteException

    await session.commit()
