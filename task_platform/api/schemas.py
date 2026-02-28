from typing import Any

from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: str
    payload: Any = None