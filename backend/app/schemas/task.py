from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskCreateSchema(BaseModel):
    """Схема для создания задачи."""

    title: str = Field(
        min_length=2,
        max_length=255,
        description="Заголовок задачи",
    )
    description: str | None = Field(
        default=None,
        max_length=5000,
        description="Описание задачи",
    )


class TaskUpdateSchema(BaseModel):
    """Схема для обновления задачи."""

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
        description="Заголовок задачи",
    )
    description: str | None = Field(
        default=None,
        max_length=5000,
        description="Описание задачи",
    )
    is_completed: bool | None = Field(
        default=None,
        description="Статус выполнения задачи",
    )

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        values = self.model_dump(exclude_unset=True)
        if not values:
            raise ValueError("Необходимо указать хотя бы одно поле для обновления")
        return self


class TaskResponseSchema(BaseModel):
    """Схема для ответа с информацией о задаче."""

    id: int = Field(
        description="Уникальный идентификатор задачи",
    )
    user_id: int = Field(
        description="ID пользователя, которому принадлежит задача",
    )
    title: str = Field(
        description="Заголовок задачи",
    )
    description: str | None = Field(
        default=None,
        description="Описание задачи",
    )
    is_completed: bool = Field(
        description="Статус выполнения задачи",
    )
    created_at: datetime = Field(
        description="Дата и время создания задачи",
    )
    updated_at: datetime = Field(
        description="Дата и время изменения задачи",
    )

    # Для конвертирования моделей SQLAlchemy в Pydantic
    model_config = ConfigDict(from_attributes=True)


class TaskListResponseSchema(BaseModel):
    """Схема для ответа со списком задач."""

    tasks: list[TaskResponseSchema] = Field(
        description="Список задач текущего пользователя",
    )
    total: int = Field(
        description="Общее количество задач текущего пользователя",
    )
