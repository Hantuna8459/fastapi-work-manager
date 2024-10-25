from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import (NotCreatorOfCategory, CategoryNotFound,
                                        UserJoinedCategory)
from backend.app.crud.category import is_creator_of_category, is_category_id_exist
from backend.app.crud.user_category import create_user_category, is_user_join_category
from backend.app.schema.user_category import UserCategorySchema


add_router = APIRouter()


@add_router.post('/add', response_model=UserCategorySchema)
async def add(user_category: UserCategorySchema,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_category_id_exist(db, user_category.category_id):
            raise CategoryNotFound

        if not await is_creator_of_category(db, user_category.category_id,
                                            user.id):
            raise NotCreatorOfCategory

        user_ids = user_category.user_ids
        category_id = user_category.category_id
        for user_id in user_ids:
            if await is_user_join_category(db, user_id, category_id):
                raise UserJoinedCategory

            await create_user_category(db, user_id, category_id)

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(user_category))