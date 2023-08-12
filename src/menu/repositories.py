from uuid import UUID

from fastapi import Depends
from sqlalchemy import and_, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.base.base_repository import BaseRepository
from src.menu.models import Dish, Menu, Submenu
from sqlalchemy.orm import selectinload


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

    async def all_menu(self) -> list[tuple[Menu]]:
        result = await self.session.execute(
            select(Menu).
            order_by(Menu.id).
            options(
                selectinload(Menu.submenus).
                selectinload(Submenu.dishes)
            )
        )
        return result.all()


class SubmenuRepository(BaseRepository):
    def __init__(self, menu_id: UUID, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session=session)
        self.model = Submenu
        self.query = select(
            self.model,
            func.count(distinct(Dish.id).label('dishes_count')),
        ).outerjoin(Dish, self.model.id == Dish.submenu_id).where(Submenu.menu_id == menu_id)
        self.name = 'submenu'


class DishRepository(BaseRepository):

    def __init__(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session=session)
        self.model = Dish
        self.menu_id = menu_id
        self.submenu_id = submenu_id
        self.query = select(self.model).where(and_(
            self.model.submenu_id == Submenu.id,
            Submenu.id == self.submenu_id,
            Submenu.menu_id == self.menu_id
        ))
        self.name = 'dish'
