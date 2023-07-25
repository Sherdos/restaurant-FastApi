from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from .utils import (
    create_dish_db, create_menu_db, create_submenu_db, delete_dish_db, 
    delete_submenu_db, get_all_dish_db, get_specific_dish_db, 
    get_specific_submenu_db, update_dish_db, update_menu_db, get_specific_menu_db, 
    get_all_menu_db, delete_menu_db, get_all_submenu_db, update_submenu_db
)
from src.database import get_async_session

from .schemas import CreateDish, CreateMenu, GetMenu, GetDish, GetSubmenu


router = APIRouter(
    prefix = '/api/v1/menus',
    tags = ["Menu"]
)



'''

CRUD Menu

'''


@router.get('/', response_model=GetMenu) 
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    result = await get_all_menu_db(session)
    return JSONResponse(result)


@router.get('/{menu_id}', response_model=GetMenu)
async def get_menu(menu_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await get_specific_menu_db(session, menu_id)
    return JSONResponse(result)


@router.post('/', response_model=GetMenu)
async def add_menu(new_menu:CreateMenu, session: AsyncSession = Depends(get_async_session)):   
    result = await create_menu_db(session, new_menu)
    return JSONResponse(result, status_code=201)


@router.patch('/{menu_id}', response_model=GetMenu)
async def update_menu(menu_id: str, updated_menu: CreateMenu, session: AsyncSession = Depends(get_async_session)):
    result = await update_menu_db(session, updated_menu, menu_id)
    return JSONResponse(result)


@router.delete('/{menu_id}')
async def delete_menu(menu_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await delete_menu_db(session, menu_id)
    return JSONResponse(result)








'''

CRUD Submenu

'''

@router.get('/{menu_id}/submenus', response_model=GetSubmenu) 
async def get_submenus(menu_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await get_all_submenu_db(session, menu_id)
    return JSONResponse(result)


@router.get('/{menu_id}/submenus/{submenu_id}', response_model=GetSubmenu)
async def get_submenu(menu_id:str, submenu_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await get_specific_submenu_db(session, menu_id, submenu_id)
    return JSONResponse(result)


@router.post('/{menu_id}/submenus', response_model=GetSubmenu)
async def add_submenu(menu_id:str, new_menu:CreateMenu, session: AsyncSession = Depends(get_async_session)):   
    result = await create_submenu_db(session,  new_menu, menu_id)
    return JSONResponse(result, status_code=201)


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=GetSubmenu)
async def update_submenu(menu_id: str, submenu_id:str, updated_submenu: CreateMenu, session: AsyncSession = Depends(get_async_session)):
    result = await update_submenu_db(session, updated_submenu, menu_id, submenu_id)
    return JSONResponse(result)


@router.delete('/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(menu_id:str, submenu_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await delete_submenu_db( session, menu_id, submenu_id )
    return JSONResponse(result)








'''

CRUD Dish

'''

@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=GetDish)
async def get_dishes(menu_id:str, submenu_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await get_all_dish_db(session, menu_id, submenu_id)
    return JSONResponse(result)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=GetDish)
async def get_dish(menu_id:str, submenu_id:str, dish_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await get_specific_dish_db(session, menu_id, submenu_id, dish_id)
    return JSONResponse(result)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', response_model=GetDish)
async def add_dish(menu_id:str, submenu_id:str, new_menu:CreateDish, session: AsyncSession = Depends(get_async_session)):   
    result = await create_dish_db(session, new_menu, menu_id, submenu_id)
    return JSONResponse(result, status_code=201)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=GetDish)
async def update_dish(menu_id: str, submenu_id:str, dish_id:str, updated_dish: CreateDish, session: AsyncSession = Depends(get_async_session)):
    result = await update_dish_db(session, updated_dish, menu_id, submenu_id, dish_id)
    return JSONResponse(result)


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(menu_id:str, submenu_id:str, dish_id:str, session: AsyncSession = Depends(get_async_session)):
    result = await delete_dish_db( session, menu_id, submenu_id, dish_id )
    return JSONResponse(result)
