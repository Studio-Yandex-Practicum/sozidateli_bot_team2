class ObjectIsNoneException(Exception):
    """Запрос к БД вернул None."""


class ObjectAlreadyExists(Exception):
    """Запрос к БД вернул не пустое значение."""


class InvalidDate(Exception):
    """Дата в меньше текущей."""


class MeetingClosed(Exception):
    """Запись на собрание закрыта."""
