from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.crud.User_Category import is_user_join_category
from backend.app.crud.Category import read_category_by_id
from backend.app.schema.Category import CategoryWithItemsSchema


detail_router = APIRouter()


@detail_router.get('/{category_id}/detail', response_model=CategoryWithItemsSchema)
async def detail(category_id: str,
                 user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_user_join_category(db, user.id, category_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this category",
            )

        category = await read_category_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(category))