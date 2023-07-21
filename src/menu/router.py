


from typing import List
from fastapi import APIRouter

from .schemas import Menu


router = APIRouter(
    prefix = '/api/v1',
    tags = ["Menu"]
)

menus = []



@router.get('/menus',response_model=List[Menu])
async def get_menus():
    return menus


@router.get('/menus/{menu_id}', response_model=Menu)
async def get_menu(menu_id:int):
    return [ i for i in menus if i['id'] == menu_id ]


@router.post('/menus', response_model=Menu)
async def add_menu(menu:Menu):    
    menus.append(menu)
    return {'added':menus}


@router.patch('/menus/{target_menu_id}', response_model=Menu)
async def update_menu(target_menu_id, menu:Menu):
    new_menu = menus[2]
    new_menu['title'] = menu.title
    new_menu['description'] = menu.description
    return new_menu


@router.delete('/menus/{target_menu_id}', response_model=Menu)
async def delete_menu(target_menu_id):
    deleted_menu = menus.pop(1)
    return {'status':200, 'data':deleted_menu}