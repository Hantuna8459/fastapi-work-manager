from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.crud.Todo_item import read_todo_item_by_id, delete_todo_item

delete_router = APIRouter()


@delete_router.delete('/{todo_item_id}/delete')
async def add(todo_item_id: str,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        todo_item = await read_todo_item_by_id(db, todo_item_id)
        if not todo_item:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Todo item not found.",
                )

        if todo_item.created_by != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this todo item."
            )

        await delete_todo_item(db, todo_item_id)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))