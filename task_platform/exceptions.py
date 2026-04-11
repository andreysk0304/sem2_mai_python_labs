class TaskPlatformError(Exception):
    """Базовый класс исключений для платформы"""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TaskSourceError(TaskPlatformError):
    """Ошибка при получении задач из источника (файл, API, генератор)"""


class InvalidTaskDataError(TaskSourceError):
    """Некорректный формат данных, ожидается массив задач с полями id и payload"""


class InvalidTaskItemError(TaskSourceError):
    """Некорректая задача, отсутствует id или неверная структура"""


class InvalidSourceConfigError(TaskSourceError):
    """Некорректная конфигурация источника (например, отрицательный count)"""


class InvalidTaskSource(TaskSourceError):
    """Некорректный истоник задач, не соблюдается TaskSourceProtocol"""


class TaskValidationError(TaskPlatformError):
    """Нарушение инварианта модели задачи"""


class HandleError(TaskPlatformError):
    """Невозможно обработать задачу"""


class ExecutorWorkersCountError(TaskPlatformError):
    """Не валидное кол-во воркеров в executor"""


class ExecutorHandlerTypeError(TaskPlatformError):
    """Не валидный типа обработчика"""