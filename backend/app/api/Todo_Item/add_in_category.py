from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import CategoryNotFound
from backend.app.crud.category import is_category_id_exist
from backend.app.crud.todo_item import create_todo_item
from backend.app.schema.todo_item import TodoItemCreateSchema, TodoItemDeepSchema


add_in_category_router = APIRouter()


@add_in_category_router.post('/add_in_category', response_model=TodoItemDeepSchema)
async def add(todo_item: TodoItemCreateSchema,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_category_id_exist(db, todo_item.category_id):
            raise CategoryNotFound

        todo_item = await create_todo_item(db, todo_item, user.id)

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_item))