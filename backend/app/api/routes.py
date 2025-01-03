# api end point here
from fastapi import APIRouter

from .utils import email_test

from .category.core import category_router
from .todo_item.core import todo_item_router
from .user_category.core import user_category_router
from .user import register, login, update
from .web_socket.core import ws_router


router = APIRouter()
router.include_router(todo_item_router)
router.include_router(category_router)
router.include_router(user_category_router)
router.include_router(ws_router)

router.include_router(register.router, tags=["accounts"])
router.include_router(login.router, tags=["accounts"])
router.include_router(update.router, tags=["accounts"])
router.include_router(email_test.router, tags=["mailing"])
