from fastapi import APIRouter
from .add import add_router
from .delete import delete_router


user_category_router = APIRouter(prefix="/user_category", tags=["User_Category"])
user_category_router.include_router(add_router)
user_category_router.include_router(delete_router)
