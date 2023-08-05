from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, delete, func, insert, select, update
from fastapi import HTTPException




async def is_title_unique(session, title, model):
    query = select(model).where(model.title == title)
    result = await session.execute(query)
    row = result.fetchone()
    return row is None



def price_rounding(row):

    dish = jsonable_encoder(row[0])

    try:
        price_float = float(dish['price'])
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid price format. Price must be a number.")
    
    rounded_price = round(price_float, 2)
    dish['price'] = "{:.2f}".format(rounded_price)

    return dish



