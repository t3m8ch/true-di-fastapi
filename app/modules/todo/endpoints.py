from fastapi import APIRouter, Depends, HTTPException

from .dto import TodoOutDTO, CreatingTodoDTO, UpdatingTodoDTO
from .services import TodosService, TodosServiceDependency, TodoNotFound

router = APIRouter(prefix="/todos")


@router.get("/", response_model=list[TodoOutDTO])
async def get_all(service: TodosService = Depends(TodosServiceDependency)) -> list[TodoOutDTO]:
    return await service.get_all()


@router.get("/{todo_id}", response_model=TodoOutDTO)
async def get_by_id(todo_id: int,
                    service: TodosService = Depends(TodosServiceDependency)) -> TodoOutDTO:
    try:
        return await service.get_by_id(todo_id)
    except TodoNotFound as e:
        raise HTTPException(status_code=404, detail=f"Todo with ID {e.todo_id} not found!")


@router.post("/", response_model=TodoOutDTO)
async def create(todo: CreatingTodoDTO,
                 service: TodosService = Depends(TodosServiceDependency)):
    return await service.create(todo)


@router.put("/{todo_id}", response_model=TodoOutDTO)
async def update(todo_id: int, todo: UpdatingTodoDTO,
                 service: TodosService = Depends(TodosServiceDependency)):
    try:
        return await service.update(todo_id, todo)
    except TodoNotFound as e:
        raise HTTPException(status_code=404, detail=f"Todo with ID {e.todo_id} not found!")


@router.delete("/{todo_id}", response_model=TodoOutDTO)
async def delete(todo_id: int, service: TodosService = Depends(TodosServiceDependency)):
    try:
        return await service.delete(todo_id)
    except TodoNotFound as e:
        raise HTTPException(status_code=404, detail=f"Todo with ID {e.todo_id} not found!")
