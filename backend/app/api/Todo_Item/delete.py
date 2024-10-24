from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import TodoItemNotFound, NotCreatorOfTodoItem
from backend.app.crud.todo_item import read_todo_item_by_id, delete_todo_item

delete_router = APIRouter()


@delete_router.delete('/{todo_item_id}/delete', response_model=dict)
async def add(todo_item_id: UUID,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        todo_item = await read_todo_item_by_id(db, todo_item_id)
        if not todo_item:
            raise TodoItemNotFound

        if todo_item.created_by != user.id:
            raise NotCreatorOfTodoItem

        await delete_todo_item(db, todo_item_id)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))