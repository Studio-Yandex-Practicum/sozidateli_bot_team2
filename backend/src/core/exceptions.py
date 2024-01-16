class ObjectIsNoneException(Exception):
    """Запрос к БД вернул None."""


class ObjectAlreadyExists(Exception):
    """Запрос к БД вернул не пустое значение."""
