from sqlalchemy import func, delete
from sqlalchemy.future import select

from backend.app.models import UserCategory
from ..schema.User_Category import UserCategorySchema
from .Crud_Core import *


async def is_user_join_category(session, user_id: str, category_id: str)\
        -> bool:

    query = (select(func.count(UserCategory.user_id))
             .where(UserCategory.user_id.__eq__(user_id)
                    & UserCategory.category_id.__eq__(category_id)))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def read_list_user_id_by_category_id(session, category_id: str)\
        -> list[str]:

    query = select(UserCategory.user_id).where(UserCategory.category_id.__eq__(category_id))
    result = await execute_with_select(session, query)
    lst = result.fetchall()
    res = []
    for x in lst:
        res.append(x[0])

    return res


async def read_list_category_id_by_user_id(session, user_id: str) \
        -> list[str]:
    query = select(UserCategory.user_id).where(UserCategory.user_id.__eq__(user_id))
    result = await execute_with_select(session, query)
    lst = result.fetchall()
    res = []
    for x in lst:
        res.append(x[0])

    return res


async def create_user_category(session, user_category: UserCategorySchema) \
        -> UserCategorySchema:

    item = UserCategory(user_id=user_category.user_id,
                        category_id=user_category.category_id)
    item = await execute_with_refresh(session, item)
    return item

async def delete_user_category(session, user_category: UserCategorySchema):
    query = (delete(UserCategory)
             .where(UserCategory.user_id.__eq__(user_category.user_id)&
                    UserCategory.category_id.__eq__(user_category.category_id)))

    await execute_with_no_refresh(session, query)