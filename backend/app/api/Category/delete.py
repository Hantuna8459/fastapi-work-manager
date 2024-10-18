from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.crud.Category import delete_category, is_creator_of_category

delete_router = APIRouter()


@delete_router.delete('/{category_id}/delete')
async def add(category_id: str,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_creator_of_category(db, category_id, user.id):
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to access this category",
                )

        await delete_category(db, category_id)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))