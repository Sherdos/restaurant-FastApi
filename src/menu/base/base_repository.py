from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.menu.models import Base
from src.menu.utils import is_title_unique


class BaseRepository():

    def __init__(self, session: AsyncSession = Depends(get_async_session), ) -> None:
        self.session: AsyncSession = session
        self.model = Base
        self.query = select()
        self.name: str

    # Это нужно чтобы pre-commit не ругался
    async def all_menu(self):
        pass

    async def get_all(self) -> list[tuple[Base]]:
        result = await self.session.execute(self.query.group_by(self.model.id))
        return result.all()

    async def get(self, id: UUID) -> tuple[Base]:
        result = await self.session.execute(self.query.where(self.model.id == id).group_by(self.model.id))
        item = result.first()
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{self.name} not found')
        return item

    async def create(self, **kwargs) -> UUID:

        if not await is_title_unique(self.session, kwargs['title'], self.model):
            raise HTTPException(status_code=404, detail='the item already exists')

        query = await self.session.execute(insert(self.model).values(**kwargs))
        item_id = query.inserted_primary_key[0]

        await self.session.commit()
        return item_id

    async def update(self, id: UUID, **kwargs) -> None:
        await self.session.execute(update(self.model).values(**kwargs).where(self.model.id == id))
        await self.session.commit()

    async def delete(self, id: UUID) -> dict:
        await self.session.execute(delete(self.model).where(self.model.id == id))
        await self.session.commit()
        return {'status': 'true', 'message': 'The object has been deleted'}
