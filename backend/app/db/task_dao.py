from app.db.base_dao import BaseDAO
from app.models import TaskModel
from app.schemas import TaskCreateSchema, TaskUpdateSchema


class TaskDAO(BaseDAO[TaskModel, TaskCreateSchema, TaskUpdateSchema]):
    """Класс для работы с задачами в базе данных."""

    model = TaskModel
