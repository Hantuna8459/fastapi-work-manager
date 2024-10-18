from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.crud.Category import is_creator_of_category
from backend.app.crud.User_Category import delete_user_category
from backend.app.schema.User_Category import UserCategorySchema


delete_router = APIRouter()


@delete_router.delete('/delete')
async def add(user_category: UserCategorySchema = Depends(),
                # user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        # if not await is_creator_of_category(db, user_category.category_id,
        #                                     user.user_id):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="You don't have permission to access this category.",
        #     )

        await delete_user_category(db, user_category)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(user_category))