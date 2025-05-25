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


class TaskCreateException(CustomException):
    """Ошибка при создании задачи."""

    def __init__(
        self,
        *,
        msg: str = "Произошла ошибка при создании задачи",
    ):
        super().__init__(msg=msg)


class TaskNotFoundException(CustomException):
    """Задача не найдена."""

    def __init__(
        self,
        *,
        msg: str = "Задача не найдена",
    ):
        super().__init__(msg=msg)


class TaskUpdateException(CustomException):
    """Ошибка при обновлении задачи."""

    def __init__(
        self,
        *,
        msg: str = "Произошла ошибка при обновлении задачи",
    ):
        super().__init__(msg=msg)


class TaskDeleteException(CustomException):
    """Ошибка при удалении задачи."""

    def __init__(
        self,
        *,
        msg: str = "Произошла ошибка при удалении задачи",
    ):
        super().__init__(msg=msg)
