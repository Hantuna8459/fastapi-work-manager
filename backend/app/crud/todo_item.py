from uuid import UUID
from sqlalchemy import func, delete, update
from sqlalchemy.future import select

from backend.app.models.todo_item import TodoItem, ItemStatus
from backend.app.core.exception import TodoItemStatusDoneException
from backend.app.schema.todo_item import *
from .core import *


async def read_todo_items(session, pagesize: int, page: int,
                         user_id: UUID = "",
                         category_id: UUID = "") \
        -> list[TodoItemSchema] | None:

    limit = pagesize
    offset = (page - 1) * pagesize

    where_clause = None
    if (user_id != "") & (category_id != ""):
        where_clause = ((TodoItem.created_by.__eq__(user_id))
                 &(TodoItem.category_id.__eq__(category_id)))

    elif (user_id != "") & (category_id == ""):
        where_clause = (TodoItem.created_by.__eq__(user_id))

    elif (user_id == "") & (category_id != ""):
        where_clause = (TodoItem.category_id.__eq__(category_id))

    query = (select(TodoItem.id, TodoItem.name,
                   TodoItem.description, TodoItem.status,
                    TodoItem.created_by, TodoItem.category_id)
             .where(where_clause).limit(limit).offset(offset))

    result = await execute_with_select(session, query)
    todo_items = result.fetchall()
    if not todo_items:
        return None

    lst = []
    for todo_item in todo_items:
        lst.append(TodoItemSchema(id=todo_item[0],name=todo_item[1],
                                  description=todo_item[2],status=todo_item[3],
                                  created_by=todo_item[4],category_id=todo_item[5]))
    return lst


async def read_todo_item_by_id(session, todo_item_id: UUID) \
        -> TodoItemDeepSchema | None:

    query = (select(TodoItem.id, TodoItem.name,
                    TodoItem.description, TodoItem.status,
                    TodoItem.created_by, TodoItem.category_id,
                    TodoItem.created_at, TodoItem.updated_at)
             .where(TodoItem.id.__eq__(todo_item_id)))

    result = await execute_with_select(session, query)
    todo_item = result.fetchone()
    if not todo_item:
        return None

    return TodoItemDeepSchema(id=todo_item[0],name=todo_item[1],
                          description=todo_item[2],status=todo_item[3],
                          created_by=todo_item[4],category_id=todo_item[5],
                          created_at=todo_item[6],updated_at=todo_item[7])


async def is_todo_item_exist(session, todo_item_id: UUID) \
        -> bool:

    query = select(func.count(TodoItem.id)).where(TodoItem.id.__eq__(todo_item_id))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def is_creator_of_todo_item(session, todo_item_id: UUID, user_id: UUID):
    query = (select(func.count(TodoItem.id))
             .where((TodoItem.id.__eq__(todo_item_id))
                    &(TodoItem.created_by.__eq__(user_id))))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def create_todo_item(session,
                           todo_item: TodoItemWithCategorySchema,
                           user_id: UUID) \
        -> TodoItemDeepSchema:

    item = TodoItem(name=todo_item.name, description=todo_item.description,
                    category_id=todo_item.category_id,created_by=user_id)

    item = await execute_with_refresh(session, item)
    return item


async def update_todo_item_status_by_id(session, todo_item_id: UUID,)\
        -> None:

    todo_item = await read_todo_item_by_id(session, todo_item_id)
    if todo_item.status == ItemStatus.Todo.value:
        new_status = ItemStatus.Processing
    elif todo_item.status == ItemStatus.Processing.value:
        new_status = ItemStatus.Done
    else:
        raise TodoItemStatusDoneException

    query = (update(TodoItem)
             .where(TodoItem.id.__eq__(todo_item_id))
             .values(status=new_status))

    await execute_with_no_refresh(session, query)


async def update_todo_item_by_id(session, todo_item_id: UUID,
                                 update_data: TodoItemBaseSchema) \
        -> None:

    query = (update(TodoItem)
             .where(TodoItem.id.__eq__(todo_item_id))
             .values(**update_data.__dict__))

    await execute_with_no_refresh(session, query)


async def delete_todo_item(session, todo_item_id: UUID)\
        -> None:

    query = delete(TodoItem).where(TodoItem.id.__eq__(todo_item_id))
    await execute_with_no_refresh(session, query)