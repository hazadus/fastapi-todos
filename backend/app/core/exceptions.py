"""Содержит базовый класс для исключений приложения."""


class CustomException(Exception):
    """В `msg` указываем сообщение об ошибке"""

    def __init__(
        self,
        *,
        msg: str,
    ):
        self.msg = msg
        super().__init__(msg)

    def __str__(self) -> str:
        return self.msg
