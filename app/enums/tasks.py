from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def values(cls) -> list:
        return list(map(lambda item: item.value, cls))  # type: ignore


class TaskStatus(BaseEnum):
    NEW = "Новая задача"
    IN_PROGRESS = "В разработке"
    COMPLETED = "Выполненная задача"


class TaskPriority(BaseEnum):
    LOW = "Низкий"
    MIDDLE = "Средний"
    HIGH = "Высокий"
