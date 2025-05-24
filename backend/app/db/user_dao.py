from app.db.base_dao import BaseDAO
from app.models import UserModel
from app.schemas import UserCreateSchema, UserUpdateSchema


class UserDAO(BaseDAO[UserModel, UserCreateSchema, UserUpdateSchema]):
    """Класс для работы с пользователями в базе данных."""

    model = UserModel
