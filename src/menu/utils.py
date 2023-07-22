from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.menu.models import menu
from fastapi import HTTPException


async def get_menu_db( session: AsyncSession, menu_id):
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    row = result.fetchone()
    specific_menu = {"id":str(row[0]), "title": row[1], "description": row[2]}
    return specific_menu


async def get_menus_db(session:AsyncSession):
    query = select(menu)
    result = await session.execute(query)
    menus_list = [{"id":str(row[0]),"title": row[1], "description": row[2]} for row in result.all()]
    return menus_list


async def add_menu_db(session:AsyncSession, new_menu):
    new_menu_dict = new_menu.dict()
    stmt = insert(menu).values(**new_menu_dict)
    result = await session.execute(stmt)
    await session.commit()
    new_menu_id = result.inserted_primary_key[0]
    new_menu_dict['id'] = str(new_menu_id)
    return new_menu_dict



async def update_menu_db(session:AsyncSession, updated_menu, menu_id):
    update_menu_data = updated_menu.dict()
    stmt = update(menu).values(**update_menu_data).where(menu.c.id == menu_id) 
    edit_menu = await session.execute(stmt)
    await session.commit()
    # if not edit_menu:
    #     raise HTTPException(status_code=404, detail="Меню с указанным id не найдено")
    return edit_menu

