from typing import Generator

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from starlette.requests import Request

from app.modules.todo.services import TodosService, TodosServiceDependency


async def _get_alchemy_session(request: Request) -> Generator[AsyncSession, None, None]:
    engine: AsyncEngine = request.app.state.alchemy_engine

    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


def _get_todos_service(
        alchemy_session: AsyncSession = Depends(_get_alchemy_session)
) -> TodosService:
    return TodosService(alchemy_session)


def inject_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[TodosServiceDependency] = _get_todos_service
