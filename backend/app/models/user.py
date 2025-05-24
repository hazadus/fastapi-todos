from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import CURRENT_TIMESTAMP_UTC
from app.models import BaseModel


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        sa.String(320),
        unique=True,
        index=True,
        nullable=False,
        comment="Электронная почта пользователя",
    )
    password_hash: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
        comment="Хэш пароля пользователя",
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=CURRENT_TIMESTAMP_UTC,
        comment="Дата и время создания пользователя",
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=CURRENT_TIMESTAMP_UTC,
        onupdate=CURRENT_TIMESTAMP_UTC,
        comment="Дата и время изменения пользователя",
    )

    tasks = relationship("TaskModel", back_populates="user")
