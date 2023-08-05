from uuid import UUID
from fastapi import APIRouter, Depends

from src.menu.services import DishService, MenuService, SubmenuService
from starlette import status


from .schemas import CreateDish, CreateMenu, GetMenu, GetDish, GetSubmenu


router = APIRouter(
    prefix = '/api/v1/menus',
    tags = ["Menu"]
)


@router.get('/', response_model=list[GetMenu], status_code=status.HTTP_200_OK, summary='список меню') 
async def get_menus(menu:MenuService = Depends()):
    return await menu.all()


@router.get('/{menu_id}', response_model=GetMenu, status_code=status.HTTP_200_OK, summary='меню')
async def get_menu(menu_id:UUID, menu:MenuService = Depends()):
    return await menu.get(menu_id)


@router.post('/', response_model=GetMenu, status_code=status.HTTP_201_CREATED, summary='создание меню')
async def add_menu(new_menu:CreateMenu, menu:MenuService = Depends()):   
    return await menu.create(**new_menu.model_dump()) 


@router.patch('/{menu_id}', response_model=GetMenu, status_code=status.HTTP_200_OK, summary='обновление меню')
async def update_menu(menu_id: UUID, updated_menu: CreateMenu, menu:MenuService = Depends()):
    return await menu.update(menu_id, **updated_menu.model_dump())


@router.delete('/{menu_id}')
async def delete_menu(menu_id: UUID, menu:MenuService = Depends()):
    return await menu.delete(menu_id)









@router.get('/{menu_id}/submenus', response_model=list[GetSubmenu]) 
async def get_submenus(menu_id:UUID, submenu:SubmenuService = Depends()):
    return await submenu.all(menu_id)


@router.get('/{menu_id}/submenus/{submenu_id}', response_model=GetSubmenu)
async def get_submenu(menu_id:UUID, submenu_id:UUID, submenu:SubmenuService = Depends()):
    return await submenu.get(menu_id, submenu_id)


@router.post('/{menu_id}/submenus', response_model=GetSubmenu, status_code=status.HTTP_201_CREATED)
async def add_submenu(menu_id:str, new_menu:CreateMenu, submenu:SubmenuService = Depends()):
    return await submenu.create(menu_id, **new_menu.model_dump())


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=GetSubmenu)
async def update_submenu(menu_id:UUID, submenu_id:UUID, updated_menu:CreateMenu, submenu:SubmenuService = Depends()):
    return await submenu.update(menu_id, submenu_id, **updated_menu.model_dump())


@router.delete('/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(submenu_id:UUID, submenu:SubmenuService = Depends()):
    return await submenu.delete(submenu_id)








'''

CRUD Dish

'''

@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[GetDish])
async def get_dishes(menu_id:UUID, submenu_id:UUID, dish:DishService = Depends()):
    return await dish.all(submenu_id)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=GetDish)
async def get_dish(menu_id:UUID, submenu_id:UUID, dish_id:UUID, dish:DishService = Depends()):
    return await dish.get(submenu_id, dish_id)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', response_model=GetDish, status_code=status.HTTP_201_CREATED)
async def add_dish(menu_id:UUID, submenu_id:UUID, new_dish:CreateDish, dish:DishService = Depends()):   
    return await dish.create(submenu_id, **new_dish.model_dump())


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=GetDish)
async def update_dish(menu_id: UUID, submenu_id:UUID, dish_id:UUID, updated_dish: CreateDish, dish:DishService = Depends()):
    return await dish.update(submenu_id, dish_id, **updated_dish.model_dump())


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(menu_id:UUID, submenu_id:UUID, dish_id:UUID, dish:DishService = Depends()):
    return await dish.delete(dish_id)
