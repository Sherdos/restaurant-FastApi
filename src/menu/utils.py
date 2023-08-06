from fastapi import HTTPException
from fastapi_cache import FastAPICache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.schemas import GetDish


async def is_title_unique(session: AsyncSession, title: str, model) -> bool:
    query = select(model).where(model.title == title)
    result = await session.execute(query)
    row = result.fetchone()
    return row is None


def price_rounding(dish: GetDish) -> GetDish:
    try:
        price_float = float(dish.price)
    except ValueError:
        raise HTTPException(status_code=404, detail='Invalid price format. Price must be a number.')

    rounded_price = round(price_float, 2)
    dish.price = f'{rounded_price:.2f}'

    return dish


async def clean_cach(*arg) -> None:
    for i in arg:
        await FastAPICache.clear(i)
