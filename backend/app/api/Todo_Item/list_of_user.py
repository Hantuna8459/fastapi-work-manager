from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.crud.Todo_item import read_todo_items


list_of_user_router = APIRouter()


@list_of_user_router.get('/list')
async def list_categories(
        pagesize: int = 5, page: int = 1,
        # user = Depends(get_current_user),
        db = Depends(get_db)
):
    try:
        # todo_items = await read_todo_items(db, pagesize, page, user.id)
        todo_items = {}
        if not todo_items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo items not found",
            )
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(todo_items))