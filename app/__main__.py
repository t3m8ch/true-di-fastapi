import uvicorn

from app.main.app import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.__main__:app", reload=True)
