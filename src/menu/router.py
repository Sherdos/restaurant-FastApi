
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import APIRouter, Depends
from .models import menu
from .utils import get_menu_db, get_menus_db, add_menu_db, update_menu_db
from src.database import get_async_session

from .schemas import CreateMenu, GetMenu


router = APIRouter(
    prefix = '/api/v1',
    tags = ["Menu"]
)




@router.get('/menus') 
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    menus_list = get_menus_db(session)
    return menus_list


@router.get('/menus/{menu_id}')
async def get_menu(menu_id:int, session: AsyncSession = Depends(get_async_session)):
    specific_menu = await get_menu_db(session, menu_id)
    return specific_menu


@router.post('/menus')
async def add_menu(new_menu:CreateMenu, session: AsyncSession = Depends(get_async_session)):   
    add_menu = add_menu_db(session, new_menu)
    return JSONResponse(content=add_menu, status_code=201)



@router.patch('/menus/{menu_id}')
async def update_menu(menu_id: int, updated_menu: CreateMenu, session: AsyncSession = Depends(get_async_session)):
    await update_menu_db(session, updated_menu, menu_id)
    edit_menu = await get_menu_db(session, menu_id)
    return edit_menu



@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id:int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(menu).where(menu.c.id == menu_id)
    result = await session.execute(stmt)
    await session.commit()
    return {'status':'success'}