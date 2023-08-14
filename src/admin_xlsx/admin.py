from uuid import UUID

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_xlsx.xlsx import from_xlsx_to_dict, get_reposytory
from src.database import get_async_session


class AdminXLSX():
    def __init__(self, repository) -> None:
        self.repository = repository

    async def create(self, session: AsyncSession, dict_obj: dict) -> UUID:
        object = self.repository(session=session)
        object_id = await object.create(**dict_obj)
        return object_id

    async def update(self, session: AsyncSession, id: UUID, dict_obj: dict) -> None:
        object = self.repository(session=session)
        await object.update(id, **dict_obj)

    async def delete(self, session: AsyncSession, id: UUID) -> None:
        object = self.repository(session=session)
        await object.delete(id)


async def update_admin():
    data = from_xlsx_to_dict()
    data_frame = pd.read_excel('admin/Menu.xlsx')
    async for session in get_async_session():
        for index, item in enumerate(data):
            repository = get_reposytory(index)
            admin = AdminXLSX(repository)
            for dict_obj in item:
                move = dict_obj.pop('move')
                if move == 'C':
                    menu_id = await admin.create(session, dict_obj)
                    data_frame.loc[
                        data_frame[f'Unnamed: {index+1}'] == dict_obj['title'], f'Unnamed: {index}'
                    ] = menu_id
                elif move == 'U':
                    await admin.update(session=session, id=dict_obj['id'], dict_obj=dict_obj)
                elif move == 'D':
                    await admin.delete(session=session, id=dict_obj['id'])
                    condition = data_frame[f'Unnamed: {index}'] == dict_obj['id']
                    indexes = data_frame.index[condition]
                    data_frame = data_frame.drop(indexes)

                data_frame.loc[data_frame['Unnamed: 7'].notna(), 'Unnamed: 7'] = None
    data_frame.to_excel('admin/Menu.xlsx', index=False)
