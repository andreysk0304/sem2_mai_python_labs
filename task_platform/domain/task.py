from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Task:
    """
    Описание типизации и полей для каждой задачи

    :param id: Уникальный индефикатор задачи
    :param payload: Некоторый произвольный набор данных задачи
    """

    id: str
    payload: Any