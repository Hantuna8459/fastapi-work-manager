from uuid import UUID
from sqlalchemy import func, delete
from sqlalchemy.future import select

from backend.app.models import UserCategory
from ..schema.user_category import UserCategorySchema
from .core import *


async def is_user_join_category(session, user_id: UUID, category_id: UUID)\
        -> bool:

    query = (select(func.count(UserCategory.user_id))
             .where(UserCategory.user_id.__eq__(user_id)
                    & UserCategory.category_id.__eq__(category_id)))
    result = await execute_with_select(session, query)
    return result.scalar() > 0


async def read_list_user_id_by_category_id(session, category_id: UUID,
                                           pagesize: int, page: int)\
        -> list[UUID]:

    limit = pagesize
    offset = (page - 1) * pagesize
    query = select(UserCategory.user_id).where(UserCategory.category_id.__eq__(category_id)
                                               .limit(limit).offset(offset))
    result = await execute_with_select(session, query)
    lst = result.fetchall()
    res = []
    for x in lst:
        res.append(x[0])

    return res


async def read_list_category_id_by_user_id(session, user_id: UUID) \
        -> list[UUID]:

    query = select(UserCategory.category_id).where(UserCategory.user_id.__eq__(user_id))
    result = await execute_with_select(session, query)
    lst = result.fetchall()
    res = []
    for x in lst:
        res.append(x[0])

    return res


async def create_user_category(session, user_id: UUID, category_id: UUID) \
        -> None:

    item = UserCategory(user_id=user_id,category_id=category_id)
    item = await execute_with_refresh(session, item)


async def delete_user_category(session, user_id: UUID, category_id: UUID):

    query = (delete(UserCategory)
            .where(UserCategory.user_id.__eq__(user_id)&
                UserCategory.category_id.__eq__(category_id)))

    await execute_with_no_refresh(session, query)