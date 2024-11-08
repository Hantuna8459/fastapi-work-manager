from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import NotCreatorOfCategory, CategoryNotFound
from backend.app.crud.category import (is_creator_of_category,
                                       update_category_by_id,
                                       is_category_id_exist)
from backend.app.schema.category import CategoryCreateSchema


update_router = APIRouter()


@update_router.post('/{category_id}/update', response_model=dict)
async def detail(category_id: UUID,
                 category: CategoryCreateSchema,
                 user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_category_id_exist(db, category_id):
            raise CategoryNotFound

        if not await is_creator_of_category(db, category_id, user.id):
            raise NotCreatorOfCategory

        await update_category_by_id(db, category_id, category)

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))