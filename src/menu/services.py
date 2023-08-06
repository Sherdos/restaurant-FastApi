from uuid import UUID

from fastapi import Depends
from fastapi_cache.decorator import cache

from src.menu.base.base_service import BaseService
from src.menu.repositories import DishRepository, MenuRepository, SubmenuRepository
from src.menu.schemas import GetDish, GetMenu, GetSubmenu


class MenuService(BaseService):

    def __init__(self, db_repository: MenuRepository = Depends()) -> None:
        super().__init__(db_repository, ['menu_list', 'menu'])

    @cache(expire=30, namespace='menu_list')
    async def all(self) -> list[GetMenu]:
        return await super().all()

    @cache(expire=30, namespace='menu')
    async def get(self, id: UUID) -> GetMenu:
        return await super().get(id)


class SubmenuService(BaseService):

    def __init__(self, db_repository: SubmenuRepository = Depends()) -> None:
        super().__init__(db_repository, ['submenu_list', 'submenu'])

    @cache(expire=30, namespace='submenu_list')
    async def all(self) -> list[GetSubmenu]:
        return await super().all()

    @cache(expire=30, namespace='submenu')
    async def get(self, id: UUID) -> GetSubmenu:
        return await super().get(id)


class DishService(BaseService):

    def __init__(self, db_repository: DishRepository = Depends()) -> None:
        super().__init__(db_repository, ['dish_list', 'dish'])

    @cache(expire=30, namespace='dish_list')
    async def all(self) -> list[GetDish]:
        return await super().all()

    @cache(expire=30, namespace='dish')
    async def get(self, id: UUID) -> GetDish:
        return await super().get(id)
