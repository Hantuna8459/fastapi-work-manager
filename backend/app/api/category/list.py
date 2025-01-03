from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import CategoryNotFound
from backend.app.crud.category import read_categories_by_user_id
from backend.app.schema.category import CategorySchema


list_router = APIRouter()


@list_router.get('/list', response_model=list[CategorySchema])
async def list_categories(
        pagesize: int = 5, page: int = 1,
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    try:
        categories = await read_categories_by_user_id(db, user.id, pagesize, page)

        if not categories:
            raise CategoryNotFound

    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(categories))