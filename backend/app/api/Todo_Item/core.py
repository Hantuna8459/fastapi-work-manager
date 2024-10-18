from fastapi import APIRouter
from .add import add_router
from .detail import detail_router
from .list_of_user import list_of_user_router
from .delete import delete_router


todo_item_router = APIRouter(prefix="/todo_item", tags=["Todo_Item"])
todo_item_router.include_router(list_of_user_router)
todo_item_router.include_router(detail_router)
todo_item_router.include_router(add_router)
todo_item_router.include_router(delete_router)
