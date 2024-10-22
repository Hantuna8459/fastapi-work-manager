from uuid import UUID
from sqlalchemy import func, delete, update
from sqlalchemy.future import select

from backend.app.models import Todo_Item
from backend.app.schema.Todo_item import *
from .core import *


async def read_todo_items(session, pagesize: int, page: int,
                         user_id: UUID = "",
                         category_id: UUID = "") \
        -> list[TodoItemSchema] | None:

    limit = pagesize
    offset = (page - 1) * pagesize

    where_clause = None
    if (user_id != "") & (category_id != ""):
        where_clause = ((Todo_Item.created_by.__eq__(user_id))
                 &(Todo_Item.category_id.__eq__(category_id)))

    elif (user_id != "") & (category_id == ""):
        where_clause = (Todo_Item.created_by.__eq__(user_id))

    elif (user_id == "") & (category_id != ""):
        where_clause = (Todo_Item.category_id.__eq__(category_id))

    query = (select(Todo_Item.id, Todo_Item.name,
                   Todo_Item.description, Todo_Item.status,
                    Todo_Item.created_by, Todo_Item.category_id)
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

    query = (select(Todo_Item.id, Todo_Item.name,
                    Todo_Item.description, Todo_Item.status,
                    Todo_Item.created_by, Todo_Item.category_id,
                    Todo_Item.created_at, Todo_Item.updated_at)
             .where(Todo_Item.id.__eq__(todo_item_id)))

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

    query = select(func.count(Todo_Item.id)).where(Todo_Item.id.__eq__(todo_item_id))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def create_todo_item(session,
                           todo_item: TodoItemCreateSchema | TodoItemBaseSchema,
                           user_id: UUID) \
        -> TodoItemDeepSchema:
    if isinstance(todo_item, TodoItemCreateSchema):
        item = Todo_Item(name=todo_item.name, description=todo_item.description,
                         category_id=todo_item.category_id,
                         created_by=user_id)

    else:
        item = Todo_Item(name=todo_item.name, description=todo_item.description,
                         created_by=user_id)

    item = await execute_with_refresh(session, item)
    return item


async def delete_todo_item(session, todo_item_id: UUID)\
        -> None:

    query = delete(Todo_Item).where(Todo_Item.id.__eq__(todo_item_id))
    await execute_with_no_refresh(session, query)