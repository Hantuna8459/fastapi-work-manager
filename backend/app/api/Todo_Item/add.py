from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.crud.Category import is_category_id_exist
from backend.app.crud.Todo_item import create_todo_item
from backend.app.schema.Todo_item import TodoItemCreateSchema, TodoItemDeepSchema, TodoItemBaseSchema

add_router = APIRouter()


@add_router.post('/add', response_model=TodoItemDeepSchema)
async def add(todo_item: TodoItemBaseSchema,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        todo_item = await create_todo_item(db, todo_item, user.id)

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_item))