"""Содержит исключения, используемые в сервисах приложения."""

from app.core.exceptions import CustomException


class EmailAlreadyExistsException(CustomException):
    """Пользователь с таким email уже существует."""

    def __init__(
        self,
        *,
        msg: str = "Пользователь с указанным email уже существует",
    ):
        super().__init__(msg=msg)


class TaskCreationException(CustomException):
    """Ошибка при создании задачи."""

    def __init__(
        self,
        *,
        msg: str = "Произошла ошибка при создании задачи",
    ):
        super().__init__(msg=msg)
