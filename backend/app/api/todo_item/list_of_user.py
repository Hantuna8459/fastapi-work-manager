from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import TodoItemNotFound
from backend.app.crud.todo_item import read_todo_items
from backend.app.schema.todo_item import TodoItemSchema


list_of_user_router = APIRouter()


@list_of_user_router.get('/list', response_model=list[TodoItemSchema])
async def list_categories(
        pagesize: int = 5, page: int = 1,
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    try:
        todo_items = await read_todo_items(db, pagesize, page, user.id)
        if not todo_items:
            raise TodoItemNotFound

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_items))