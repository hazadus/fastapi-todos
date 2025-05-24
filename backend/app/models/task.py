from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import CURRENT_TIMESTAMP_UTC
from app.models import BaseModel


class TaskModel(BaseModel):
    """Модель задачи."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя, которому принадлежит задача",
    )
    title: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
        comment="Заголовок задачи",
    )
    description: Mapped[str] = mapped_column(
        sa.Text,
        nullable=True,
        comment="Описание задачи",
    )
    is_completed: Mapped[bool] = mapped_column(
        default=False,
        comment="Статус выполнения задачи",
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=CURRENT_TIMESTAMP_UTC,
        comment="Дата и время создания задачи",
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=CURRENT_TIMESTAMP_UTC,
        onupdate=CURRENT_TIMESTAMP_UTC,
        comment="Дата и время изменения задачи",
    )

    user = relationship("UserModel", back_populates="tasks")
