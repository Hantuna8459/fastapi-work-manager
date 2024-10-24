from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import TodoItemNotFound, CantAccessTodoItem
from backend.app.crud.user_category import is_user_join_category
from backend.app.crud.todo_item import read_todo_item_by_id
from backend.app.schema.todo_item import TodoItemDeepSchema


detail_router = APIRouter()


@detail_router.get('/{todo_item_id}/detail', response_model=TodoItemDeepSchema)
async def detail(todo_item_id: UUID,
                 user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:

        todo_item = await read_todo_item_by_id(db, todo_item_id)
        if not todo_item:
            raise TodoItemNotFound

        if todo_item.category_id:
            if not await is_user_join_category(db, user.id, todo_item.category_id):
                raise CantAccessTodoItem

        if todo_item.created_by != user.id:
            raise CantAccessTodoItem

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_item))