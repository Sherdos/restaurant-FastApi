from fastapi import Depends
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.base.base_repository import BaseRepository
from src.menu.models import Dish, Menu, Submenu


class MenuRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session=session)
        self.model = Menu
        self.query = select(
            Menu,
            func.count(distinct(Submenu.id).label('submenus_count')),
            func.count(distinct(Dish.id).label('dishes_count')),) \
            .outerjoin(Submenu, Menu.id == Submenu.menu_id) \
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        self.name = 'menu'


class SubmenuRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session=session)
        self.model = Submenu
        self.query = select(
            self.model,
            func.count(distinct(Dish.id).label('dishes_count')),
        ).outerjoin(Dish, self.model.id == Dish.submenu_id)
        self.name = 'submenu'


class DishRepository(BaseRepository):

    def __init__(self, session: AsyncSession = Depends(get_async_session),) -> None:
        super().__init__(session=session)
        self.model = Dish
        self.query = select(self.model)
        self.name = 'dish'
