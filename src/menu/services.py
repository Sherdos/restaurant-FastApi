from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi_cache.decorator import cache

from src.menu.base.base_service import BaseService
from src.menu.repositories import DishRepository, MenuRepository, SubmenuRepository
from src.menu.schemas import AllMenu, GetDish, GetMenu, GetSubmenu
from src.menu.utils import price_rounding


class MenuService(BaseService):

    def __init__(self, background_tasks: BackgroundTasks, db_repository: MenuRepository = Depends()) -> None:
        super().__init__(background_tasks, db_repository, ['menu_list', 'menu'])

    async def all_menu(self) -> list[AllMenu]:
        result = await self.db_repository.all_menu()
        return [i[0].json_mapping_all() for i in result]

    @cache(expire=30, namespace='menu_list')
    async def all(self) -> list[GetMenu]:
        return await super().all()

    @cache(expire=30, namespace='menu')
    async def get(self, id: UUID) -> GetMenu:
        return await super().get(id)


class SubmenuService(BaseService):

    def __init__(self, background_tasks: BackgroundTasks, db_repository: SubmenuRepository = Depends()) -> None:
        super().__init__(background_tasks, db_repository, ['submenu_list', 'submenu'])

    @cache(expire=30, namespace='submenu_list')
    async def all(self) -> list[GetSubmenu]:
        return await super().all()

    @cache(expire=30, namespace='submenu')
    async def get(self, id: UUID) -> GetSubmenu:
        return await super().get(id)


class DishService(BaseService):

    def __init__(self, background_tasks: BackgroundTasks, db_repository: DishRepository = Depends()) -> None:
        super().__init__(background_tasks, db_repository, ['dish_list', 'dish'])

    @cache(expire=30, namespace='dish_list')
    async def all(self) -> list[GetDish]:
        return [price_rounding(i) for i in await super().all()]

    @cache(expire=30, namespace='dish')
    async def get(self, id: UUID) -> GetDish:
        return price_rounding(await super().get(id))
