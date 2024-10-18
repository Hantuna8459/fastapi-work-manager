# api end point here
from fastapi import APIRouter
from .Category.core import category_router
from .Todo_Item.core import todo_item_router
from .User_Category.core import user_category_router


router = APIRouter()
router.include_router(todo_item_router)
router.include_router(category_router)
router.include_router(user_category_router)