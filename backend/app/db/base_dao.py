from typing import Any, Generic, TypeVar

from app.models import BaseModel
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс DAO (Data Access Object) для работы с моделями SQLAlchemy."""

    model = None

    # MARK: Create
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: CreateSchemaType | dict[str, Any],
    ) -> ModelType | None:
        """Добавляет новый объект в базу данных.

        Args:
            session: Асинхронная сессия SQLAlchemy
            obj_in: Данные для создания объекта (схема Pydantic или словарь)

        Returns:
            Созданный объект или None
        """

        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        stmt = insert(cls.model).values(**create_data).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().first()

    # MARK: Read
    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filter,
        **filter_by,
    ) -> ModelType | None:
        """Находит один объект по заданным условиям фильтрации.

        Args:
            session: Асинхронная сессия SQLAlchemy
            filter: Условия фильтрации
            filter_by: Именованные условия фильтрации

        Returns:
            Найденный объект или None
        """

        stmt = select(cls.model).filter(*filter).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        *filter,
        offset: int | None = None,
        limit: int | None = None,
        **filter_by,
    ) -> list[ModelType] | None:
        """Находит все объекты, соответствующие условиям фильтрации.

        Args:
            session: Асинхронная сессия SQLAlchemy
            filter: Условия фильтрации
            offset: Смещение для пагинации
            limit: Ограничение количества возвращаемых объектов
            filter_by: Именованные условия фильтрации

        Returns:
            Список найденных объектов или None
        """

        stmt = select(cls.model).filter(*filter).filter_by(**filter_by)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        return result.scalars().all()

    # MARK: Update
    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType | None:
        """Обновляет объект в базе данных.

        Args:
            session: Асинхронная сессия SQLAlchemy
            where: Условия для выбора обновляемого объекта
            obj_in: Данные для обновления (схема Pydantic или словарь)

        Returns:
            Обновленный объект или None
        """

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        stmt = (
            update(cls.model).where(*where).values(**update_data).returning(cls.model)
        )
        result = await session.execute(stmt)
        return result.scalars().one()

    # MARK: Delete
    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        *filter,
        **filter_by,
    ) -> int:
        """Удаляет объекты, соответствующие условиям фильтрации.

        Args:
            session: Асинхронная сессия SQLAlchemy
            filter: Условия фильтрации
            filter_by: Именованные условия фильтрации

        Returns:
            Количество удаленных строк
        """

        stmt = delete(cls.model).filter(*filter).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.rowcount
