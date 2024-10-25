from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import NotCreatorOfTodoItem, TodoItemStatusDoneException
from backend.app.crud.todo_item import (is_creator_of_todo_item,
                                        update_todo_item_status_by_id)

update_status_router = APIRouter()


@update_status_router.post('/{todo_item_id}/update_status', response_model=dict)
async def detail(todo_item_id: UUID,
                 user=Depends(get_current_user),
                 db=Depends(get_db)):
    try:
        if not await is_creator_of_todo_item(db, todo_item_id, user.id):
            raise NotCreatorOfTodoItem

        await update_todo_item_status_by_id(db, todo_item_id)

    except (DatabaseExecutionException, TodoItemStatusDoneException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))