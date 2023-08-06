from uuid import UUID

from src.menu.repositories import BaseRepository
from src.menu.schemas import Base
from src.menu.utils import clean_cach


class BaseService():

    def __init__(self, db_repository: BaseRepository, cache_names: list) -> None:
        self.db_repository = db_repository
        self.cache_names = cache_names

    async def all(self) -> list[Base]:
        result = await self.db_repository.get_all()
        return [i[0].json_mapping(i) for i in result]

    async def get(self, id: UUID) -> Base:
        result = await self.db_repository.get(id)
        return result[0].json_mapping(result)

    async def create(self, **kwargs) -> Base:
        result = await self.db_repository.create(**kwargs)
        await clean_cach(self.cache_names[0])
        return await self.get(result)

    async def update(self, id: UUID, **kwargs) -> Base:
        await self.db_repository.update(id, **kwargs)
        await clean_cach(*self.cache_names)
        return await self.get(id)

    async def delete(self, id: UUID) -> dict:
        result = await self.db_repository.delete(id)
        await clean_cach(*self.cache_names)
        return result
