from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.crud.User_Category import is_user_join_category
from backend.app.crud.Todo_item import read_todo_item_by_id
from backend.app.schema.Todo_item import TodoItemDeepSchema


detail_router = APIRouter()


@detail_router.get('/{todo_item_id}/detail', response_model=TodoItemDeepSchema)
async def detail(todo_item_id: str,
                 user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        todo_item = await read_todo_item_by_id(db, todo_item_id)
        if not todo_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo item not found",
            )

        CantAcessException = HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to access this todo item",
                )

        if todo_item.category_id:
            if not await is_user_join_category(db, user.id, todo_item.category_id):
                raise CantAcessException

        if todo_item.created_by != user.id:
            raise CantAcessException

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_item))