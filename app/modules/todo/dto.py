from typing import Optional

from pydantic import BaseModel


class TodoOutDTO(BaseModel):
    id: int
    text: str
    is_completed: bool


class CreatingTodoDTO(BaseModel):
    text: str
    is_completed: bool = False


class UpdatingTodoDTO(BaseModel):
    text: Optional[str]
    is_completed: Optional[bool]
