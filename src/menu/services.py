
from src.menu.models import Dish, Menu, Submenu
from src.menu.repositories import DishRepository, MenuRepository, SubmenuRepository
from fastapi import Depends

from src.menu.schemas import GetMenu


class MenuService:


    def __init__(self, db_repository: MenuRepository = Depends()) -> None:
        self.db_repository = db_repository

    async def all(self):
        result = await self.db_repository.get_all()
        print(result)
        return [ Menu.json_mapping(i) for i in result ]
    
    async def get(self, id):
        result = await self.db_repository.get(id)
        return Menu.json_mapping(result)
        
    async def create(self, **kwargs):
        result = await self.db_repository.create(**kwargs)
        return await self.get(result)
    
    async def update(self, menu_id, **kwargs):
        await self.db_repository.update(menu_id, **kwargs)
        return await self.get(menu_id)
    
    async def delete(self, menu_id):
        result = await self.db_repository.delete(menu_id)
        return result


class SubmenuService:


    def __init__(self, db_repository: SubmenuRepository = Depends()) -> None:
        self.db_repository = db_repository

    async def all(self, menu_id):
        result = await self.db_repository.get_all(menu_id)
        return [ Submenu.json_mapping(i) for i in result ]
    
    async def get(self,menu_id, id):
        result = await self.db_repository.get(menu_id, id)
        return Submenu.json_mapping(result)
        
    async def create(self, menu_id, **kwargs):
        result = await self.db_repository.create(menu_id=menu_id, **kwargs)
        return await self.get(menu_id, result)
    
    async def update(self, menu_id, id, **kwargs):
        await self.db_repository.update(id, **kwargs)
        return await self.get(menu_id, id)
    
    async def delete(self, id):
        result = await self.db_repository.delete(id)
        return result



class DishService:


    def __init__(self, db_repository: DishRepository = Depends()) -> None:
        self.db_repository = db_repository

    async def all(self, submenu_id):
        result = await self.db_repository.get_all(submenu_id)
        return [ Dish.json_mapping(i) for i in result ]
    
    async def get(self, submenu_id, id):
        result = await self.db_repository.get(submenu_id, id)
        return Dish.json_mapping(result)
        
    async def create(self, submenu_id, **kwargs):
        result = await self.db_repository.create(submenu_id = submenu_id,**kwargs)
        return await self.get(submenu_id, result)
    
    async def update(self, submenu_id, id, **kwargs):
        await self.db_repository.update(id, **kwargs)
        return await self.get(submenu_id, id)
    
    async def delete(self, id):
        result = await self.db_repository.delete(id)
        return result
