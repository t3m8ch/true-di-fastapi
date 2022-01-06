from fastapi import FastAPI

from app.modules.todo.endpoints import router as todo_router


def include_routers(app: FastAPI) -> None:
    app.include_router(todo_router)
