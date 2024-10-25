from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import NotCreatorOfCategory
from backend.app.crud.category import is_creator_of_category
from backend.app.crud.user_category import delete_user_category
from backend.app.schema.user_category import UserCategorySchema


delete_router = APIRouter()


@delete_router.delete('/delete', response_model=UserCategorySchema)
async def add(user_category: UserCategorySchema,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_creator_of_category(db, user_category.category_id,
                                            user.user_id):
            raise NotCreatorOfCategory

        await delete_user_category(db, user_category)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(user_category))