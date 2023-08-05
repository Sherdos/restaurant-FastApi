from sqlalchemy import and_, delete, distinct, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from src.database import get_async_session
from src.menu.models import Dish, Menu, Submenu
from src.menu.utils import is_title_unique

from starlette import status



class BaseRepository():
    def __init__(self, model, session: AsyncSession = Depends(get_async_session), ) -> None:
        self.session:AsyncSession = session
        self.model  = model

    async def get(self, query):
        item = query.first()
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Item not found')
        return item
    


    async def create(self, **kwargs):

        if not await is_title_unique(self.session, kwargs['title'], Menu):
            raise HTTPException( status_code=404, detail="the item already exists" )
        
        query = await self.session.execute(
            insert( self.model ).values(**kwargs)
        )
        item_id = query.inserted_primary_key[0]
        await self.session.commit()
        return item_id
    

    
    async def update(self, id, **kwargs):
        await self.session.execute( 
            update(self.model).values(**kwargs).where(self.model.id == id) 
        )
        await self.session.commit()



    async def delete(self, id):
        await self.session.execute( 
            delete(self.model).where(self.model.id == id) 
        )
        await self.session.commit()
        return  { "status": 'true', "message": "The object has been deleted"}


class MenuRepository(BaseRepository):

    def __init__(self, model = Menu, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(model, session)


    async def get_all(self) -> list[Menu]:
        query = await self.session.execute(
            select(
                Menu,
                func.count(distinct(Submenu.id).label('submenus_count')),
                func.count(distinct(Dish.id).label('dishes_count')),
            )
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .group_by(Menu.id)
        
        )
        return query.all()
    

    
    async def get(self, id) -> Menu:
        query = await self.session.execute(
            select(
                Menu,
                func.count(distinct(Submenu.id).label('submenus_count')),
                func.count(distinct(Dish.id).label('dishes_count')),
            )
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Menu.id == id)
            .group_by(Menu.id)
        )
        item = await super().get(query)
        return item



class SubmenuRepository(BaseRepository):

    def __init__(self, model = Submenu, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(model, session)



    async def get_all(self, menu_id) -> list[Submenu]:
        query = await self.session.execute(
            select(
                Submenu,
                func.count(distinct(Dish.id).label('dishes_count')),
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(menu_id == Submenu.menu_id)
            .group_by(Submenu.id)
        )
        return query.all()
    

    
    async def get(self, menu_id, id) -> Submenu:
        query = await self.session.execute(
            select(
                Submenu,
                func.count(distinct(Dish.id).label('dishes_count')),
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(and_(Submenu.id == id, Submenu.menu_id == menu_id))
            .group_by(Submenu.id)
        )
        item = await super().get(query)
        return item



class DishRepository(BaseRepository):

    def __init__(self, model = Dish, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(model, session)



    async def get_all(self, submenu_id) -> list[Dish]:
        query = await self.session.execute(
           select(
                Dish
            )
            .where(and_(Dish.submenu_id == submenu_id))
            .group_by(Dish.id)
        
        )
        return query.all()
    

    
    async def get(self, submenu_id, id) -> Dish:
        query = await self.session.execute(
            select(
                Dish
            )
            .where(and_(Dish.id == id, Dish.submenu_id == submenu_id))
            .group_by(Dish.id)
        )
        item = await super().get(query)
        return item