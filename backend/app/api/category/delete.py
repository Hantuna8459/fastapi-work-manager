from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import NotCreatorOfCategory
from backend.app.crud.category import delete_category, is_creator_of_category

delete_router = APIRouter()


@delete_router.delete('/{category_id}/delete', response_model=dict)
async def add(category_id: UUID,
                user = Depends(get_current_user),
                 db=Depends(get_db)):

    try:
        if not await is_creator_of_category(db, category_id, user.id):
            raise NotCreatorOfCategory

        await delete_category(db, category_id)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))