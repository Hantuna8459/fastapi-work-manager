from fastapi import APIRouter
from .add import add_router
from .detail import detail_router
from .list import list_router
from .delete import delete_router
from .list_user import list_user_router
from .update import update_router


category_router = APIRouter(prefix="/category", tags=["Category"])
category_router.include_router(list_router)
category_router.include_router(detail_router)
category_router.include_router(add_router)
category_router.include_router(update_router)
category_router.include_router(delete_router)
category_router.include_router(list_user_router)
