from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import CantAccessCategory, CategoryNotFound
from backend.app.crud.user_category import is_user_join_category
from backend.app.crud.category import read_category_by_id
from backend.app.schema.category import CategoryWithItemsSchema


detail_router = APIRouter()


@detail_router.get('/{category_id}/detail', response_model=CategoryWithItemsSchema)
async def detail(category_id: UUID,
                 user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_user_join_category(db, user.id, category_id):
            raise CantAccessCategory

        category = await read_category_by_id(db, category_id)
        if not category:
            raise CategoryNotFound

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(category))