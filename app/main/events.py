from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.modules.model_base import Base


def register_events_handlers(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup():
        alchemy_engine = create_async_engine("postgresql+asyncpg://localhost/true_di")

        async with alchemy_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

        app.state.alchemy_engine = alchemy_engine

    @app.on_event("shutdown")
    async def shutdown():
        alchemy_engine: AsyncEngine = app.state.alchemy_engine
        await alchemy_engine.dispose()
