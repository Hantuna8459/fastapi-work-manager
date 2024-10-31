from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.main import ws_manager
from backend.app.utils import send_mail
from backend.app.core.database import get_db, DatabaseExecutionException
from backend.app.core.auth import get_current_user
from backend.app.core.exception import (NotCreatorOfTodoItem,
                                        TodoItemStatusDoneException,
                                        TodoItemNotFound)
from backend.app.crud.user import read_list_email_by_list_user_id
from backend.app.crud.todo_item import (read_todo_item_by_id,
                                        is_creator_of_todo_item,
                                        update_todo_item_status_by_id)

update_status_router = APIRouter()


@update_status_router.post('/{todo_item_id}/update_status', response_model=dict)
async def detail(todo_item_id: UUID,
                 user=Depends(get_current_user),
                 db=Depends(get_db)):

    user_id = user.id
    try:
        todo_item = await read_todo_item_by_id(db, todo_item_id)
        if not todo_item:
            raise TodoItemNotFound

        if not await is_creator_of_todo_item(db, todo_item_id, user_id):
            raise NotCreatorOfTodoItem

        await update_todo_item_status_by_id(db, todo_item_id)

        # notify
        category_id = todo_item.category_id
        message = (f"From {category_id}: {user_id} just change status of "
                   f"TodoItem id: {todo_item.id} name: {todo_item.name}")

        # websocket
        ws_manager.notify(category_id, message)

        # email
        offline_user = ws_manager.get_offline_user_ids(category_id)
        lst = await read_list_email_by_list_user_id(db, offline_user)
        for tup in lst:
            send_mail(email_to=tup[0], subject="TodoItem Status Change", html_content=message)

    except (DatabaseExecutionException, TodoItemStatusDoneException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return JSONResponse(jsonable_encoder({"status": "OK"}))