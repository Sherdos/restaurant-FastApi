from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.menu.services import DishService, MenuService, SubmenuService

from .schemas import CreateDish, CreateMenu, GetDish, GetMenu, GetSubmenu, AllMenu

router_menu = APIRouter(
    prefix='/api/v1/menus',
    tags=['Menu']
)

@router_menu.get('/all', response_model=list[AllMenu])
async def get_menus_all(menu: MenuService = Depends()) -> list[AllMenu]:
    return await menu.all_menu()

@router_menu.get('', response_model=list[GetMenu])
async def get_menus(menu: MenuService = Depends()) -> list[GetMenu]:
    return await menu.all()


@router_menu.get('/{menu_id}', response_model=GetMenu)
async def get_menu(menu_id: UUID, menu: MenuService = Depends()) -> GetMenu:
    return await menu.get(menu_id)


@router_menu.post('', response_model=GetMenu, status_code=status.HTTP_201_CREATED)
async def add_menu(new_menu: CreateMenu, menu: MenuService = Depends()) -> GetMenu:
    return await menu.create(**new_menu.model_dump())


@router_menu.patch('/{menu_id}', response_model=GetMenu)
async def update_menu(menu_id: UUID, updated_menu: CreateMenu, menu: MenuService = Depends()) -> GetMenu:
    return await menu.update(menu_id, **updated_menu.model_dump())


@router_menu.delete('/{menu_id}')
async def delete_menu(menu_id: UUID, menu: MenuService = Depends()) -> dict:
    return await menu.delete(menu_id)




router_submenu = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['Submenu']
)


'''

Submenu

'''


@router_submenu.get('', response_model=list[GetSubmenu])
async def get_submenus(submenu: SubmenuService = Depends()) -> list[GetSubmenu]:
    return await submenu.all()


@router_submenu.get('/{submenu_id}', response_model=GetSubmenu)
async def get_submenu(submenu_id: UUID, submenu: SubmenuService = Depends()) -> GetSubmenu:
    return await submenu.get(submenu_id)


@router_submenu.post('', response_model=GetSubmenu, status_code=status.HTTP_201_CREATED)
async def add_submenu(menu_id: UUID, new_menu: CreateMenu, submenu: SubmenuService = Depends()) -> GetSubmenu:
    return await submenu.create(menu_id=menu_id, **new_menu.model_dump())


@router_submenu.patch('/{submenu_id}', response_model=GetSubmenu)
async def update_submenu(submenu_id: UUID, updated_menu: CreateMenu, submenu: SubmenuService = Depends()) -> GetSubmenu:
    return await submenu.update(submenu_id, **updated_menu.model_dump())


@router_submenu.delete('/{submenu_id}')
async def delete_submenu(submenu_id: UUID, submenu: SubmenuService = Depends()) -> dict:
    return await submenu.delete(submenu_id)




router_dish = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dish']
)


'''

CRUD Dish

'''


@router_dish.get('', response_model=list[GetDish])
async def get_dishes(dish: DishService = Depends()) -> list[GetDish]:
    return await dish.all()


@router_dish.get('/{dish_id}', response_model=GetDish)
async def get_dish(dish_id: UUID, dish: DishService = Depends()) -> GetDish:
    return await dish.get(dish_id)


@router_dish.post('', response_model=GetDish, status_code=status.HTTP_201_CREATED)
async def add_dish(submenu_id: UUID, new_dish: CreateDish, dish: DishService = Depends()) -> GetDish:
    return await dish.create(submenu_id=submenu_id, **new_dish.model_dump())


@router_dish.patch('/{dish_id}', response_model=GetDish)
async def update_dish(dish_id: UUID, updated_dish: CreateDish, dish: DishService = Depends()) -> GetDish:
    return await dish.update(dish_id, **updated_dish.model_dump())


@router_dish.delete('/{dish_id}')
async def delete_dish(dish_id: UUID, dish: DishService = Depends()) -> dict:
    return await dish.delete(dish_id)
