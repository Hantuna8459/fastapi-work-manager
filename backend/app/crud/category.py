from uuid import UUID
from sqlalchemy import func, delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.app.model import Category
from .user_category import read_list_category_id_by_user_id
from .core import *
from ..schema.category import *
from ..schema.todo_item import TodoItemSchema


async def read_categories_by_user_id(session, user_id: UUID) \
        -> list[CategorySchema] | None:

    lst = await read_list_category_id_by_user_id(session, user_id)
    query = (select(Category.id, Category.name, Category.description,
                    Category.created_by, Category.updated_at)
             .where(Category.id.in_(lst)))

    result = await execute_with_select(session, query)
    categories = result.fetchall()
    if not categories:
        return None

    lst = []
    for category in categories:
        lst.append(CategorySchema(id=category[0],name=category[1],
                                  description=category[2],created_by=category[3],
                                  updated_at=category[4]))

    return lst


async def read_category_by_id(session, category_id: UUID) \
        -> CategoryWithItemsSchema | None:

    query = (select(Category.id, Category.name, Category.description,
                    Category.created_by, Category.created_at,Category.updated_at)
             .where(Category.id.__eq__(category_id)))

    result = await execute_with_select(session, query)
    category = result.fetchone()

    if not category:
        return None
    return CategoryWithItemsSchema(id=category[0],name=category[1],
                                  description=category[2],created_by=category[3],
                                  created_at=category[4],updated_at=category[5])


async def is_category_id_exist(session, category_id: UUID) \
        -> bool:

    query = select(func.count(Category.id)).where(Category.id.__eq__(category_id))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def is_category_name_is_used(session, category_name: str) \
        -> bool:

    query = select(func.count(Category.name)).where(Category.name.__eq__(category_name))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def is_creator_of_category(session, category_id: UUID, user_id: UUID) \
        -> bool:

    query = (select(func.count(Category.id))
             .where(Category.id.__eq__(category_id)
                    & Category.created_by.__eq__(user_id)))

    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def create_category(session, category: CategoryCreateSchema,
                          user_id: str) \
        -> CategorySchema:

    category = Category(name=category.name,
                        description=category.description,created_by=user_id)

    category = await execute_with_refresh(session, category)
    return category


async def update_category_by_id(session, category_id: UUID,
                                update_data: CategoryCreateSchema) \
        -> None:

    query = (update(Category)
             .where(Category.id.__eq__(category_id))
             .values(**update_data.__dict__))

    await execute_with_no_refresh(session, query)


async def delete_category(session, category_id: UUID)\
        -> None:

    query = delete(Category).where(Category.id.__eq__(category_id))
    await execute_with_no_refresh(session, query)