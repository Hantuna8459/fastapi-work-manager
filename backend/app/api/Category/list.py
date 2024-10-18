from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.crud.Category import read_categories_by_user_id


list_router = APIRouter()


@list_router.get('/list')
async def list_categories(
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    try:
        categories = await read_categories_by_user_id(db, user.id)

        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categories not found",
            )
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder(categories))