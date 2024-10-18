from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.crud.Category import create_category, is_category_name_is_used
from backend.app.crud.User_Category import create_user_category
from backend.app.schema.Category import CategoryCreateSchema
from backend.app.schema.User_Category import UserCategorySchema


add_router = APIRouter()


@add_router.post('/add')
async def add(category: CategoryCreateSchema = Depends(),
                # user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if await is_category_name_is_used(db, category.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category is already used",
            )

        # category = await create_category(db, category, user.id)
        # user_category = await create_user_category(
        #     db, UserCategorySchema(category_id=category.id,user_id=user.id)
        # )

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(category))