from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import CantAccessCategory, CategoryNotFound
from backend.app.crud.category import is_category_id_exist
from backend.app.crud.user_category import (
    is_user_join_category,read_list_user_id_by_category_id)


list_user_router = APIRouter()


@list_user_router.get('/{category_id}/list_user', response_model=list[UUID])
async def list_categories(category_id: UUID,
                          pagesize: int = 10, page: int = 1,
                          user = Depends(get_current_user),
                          db = Depends(get_db)
):
    try:
        if not await is_category_id_exist(db, category_id):
            raise CategoryNotFound

        if not await is_user_join_category(db, user.id, category_id):
            raise CantAccessCategory

        lst = await read_list_user_id_by_category_id(db, category_id, pagesize, page)

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(lst))