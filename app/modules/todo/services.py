from dataclasses import dataclass

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from .dto import TodoOutDTO, CreatingTodoDTO, UpdatingTodoDTO
from .models import Todo


@dataclass
class TodoNotFound(Exception):
    todo_id: int


class TodosServiceDependency:
    pass


class TodosService:
    def __init__(self, alchemy_session: AsyncSession):
        self._session = alchemy_session

    async def get_all(self) -> list[TodoOutDTO]:
        todos = await self._session.scalars(select(Todo))
        return [_map_model(t) for t in todos]

    async def get_by_id(self, todo_id: int) -> TodoOutDTO:
        result = await self._session.get(Todo, todo_id)
        _ensure_that_result_is_not_null(result, todo_id)

        return _map_model(result)

    async def create(self, todo: CreatingTodoDTO) -> TodoOutDTO:
        result = await self._session.execute(
            insert(Todo).values(todo.dict()).returning(Todo)
        )
        await self._session.commit()
        return _map_model(result.one())

    async def update(self, todo_id: int, todo: UpdatingTodoDTO) -> TodoOutDTO:
        result = await self._session.execute(
            update(Todo)
            .values(todo.dict(exclude_unset=True))
            .where(Todo.id == todo_id)
            .returning(Todo)
        )
        await self._session.commit()
        return _map_model(_get_one(result, todo_id))

    async def delete(self, todo_id: int) -> TodoOutDTO:
        result = await self._session.execute(
            delete(Todo).where(Todo.id == todo_id).returning(Todo)
        )
        await self._session.commit()
        return _map_model(_get_one(result, todo_id))


def _map_model(todo: Todo) -> TodoOutDTO:
    return TodoOutDTO(id=todo.id, text=todo.text, is_completed=todo.is_completed)


def _ensure_that_result_is_not_null(result, todo_id: int) -> None:
    if result is None:
        raise TodoNotFound(todo_id=todo_id)


def _get_one(result, todo_id: int):
    try:
        return result.one()
    except NoResultFound:
        raise TodoNotFound(todo_id=todo_id)
