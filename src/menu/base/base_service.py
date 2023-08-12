from uuid import UUID

from fastapi import BackgroundTasks

from src.menu.repositories import BaseRepository
from src.menu.schemas import Base, AllMenu
from src.menu.utils import clean_cach


class BaseService():

    def __init__(self, background_tasks:BackgroundTasks, db_repository: BaseRepository, cache_conf: list) -> None:
        self.db_repository = db_repository
        self.cache_conf = cache_conf
        self.background_tasks = background_tasks

    async def all_menu(self) -> list[AllMenu]:
        result = await self.db_repository.all_menu()
        return [i[0].json_mapping_all() for i in result]

    async def all(self) -> list[Base]:
        result = await self.db_repository.get_all()
        return [i[0].json_mapping(i) for i in result]

    async def get(self, id: UUID) -> Base:
        result = await self.db_repository.get(id)
        return result[0].json_mapping(result)

    async def create(self, **kwargs) -> Base:
        result = await self.db_repository.create(**kwargs)
        self.background_tasks.add_task(clean_cach, self.cache_conf[0])
        return await self.get(result)

    async def update(self, id: UUID, **kwargs) -> Base:
        await self.db_repository.update(id, **kwargs)
        self.background_tasks.add_task(clean_cach, *self.cache_conf)
        return await self.get(id)

    async def delete(self, id: UUID) -> dict:
        result = await self.db_repository.delete(id)
        self.background_tasks.add_task(clean_cach, *self.cache_conf)
        return result
