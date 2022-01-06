from fastapi import FastAPI

from .routing import include_routers
from .di import inject_dependencies
from .events import register_events_handlers


def create_app() -> FastAPI:
    app = FastAPI()

    register_events_handlers(app)
    inject_dependencies(app)
    include_routers(app)

    return app
