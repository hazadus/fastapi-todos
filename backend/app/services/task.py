from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import TaskDAO
from app.schemas import TaskCreateSchema, TaskResponseSchema
from app.services.exceptions import TaskCreationException


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
        TaskCreationException: Если задача не была создана
    """
    db_task = await TaskDAO.add(
        session=session,
        obj_in={
            **task_data.model_dump(exclude_unset=True),
            "user_id": user_id,
        },
    )
    if not db_task:
        raise TaskCreationException

    try:
        response_data = TaskResponseSchema.model_validate(db_task)
    except ValidationError as e:
        raise TaskCreationException from e

    await session.commit()
    return response_data


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
