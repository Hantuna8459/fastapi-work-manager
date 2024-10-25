from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import CantAccessCategory, TodoItemNotFound
from backend.app.crud.user_category import is_user_join_category
from backend.app.crud.todo_item import read_todo_items
from backend.app.schema.todo_item import TodoItemSchema

list_of_category_router = APIRouter()


@list_of_category_router.get('/{category_id}/list_todo_item',
                         response_model=list[TodoItemSchema])

async def list_categories(
        category_id: UUID,
        pagesize: int = 5, page: int = 1,
        user=Depends(get_current_user),
        db=Depends(get_db)
):

    try:
        if not await is_user_join_category(db, user.id, category_id):
            raise CantAccessCategory

        todo_items = await read_todo_items(db, pagesize, page, None, category_id)
        if not todo_items:
            raise TodoItemNotFound

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_items))