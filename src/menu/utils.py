from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.menu.models import Menu, Submenu, Dish
from fastapi import HTTPException


'''

Запросы по вычислении количества подменю и блюд

'''

dish_subquery = (
        select(func.count())
        .where(Dish.submenu_id == Submenu.id)
        .correlate(Submenu)
        .label("colum")
    )

submenu_subquery = (
    select(func.count()).where(Submenu.menu_id == Menu.id)
    .correlate(Menu)
    .label("submenuCount")
    )

sub_dish_subquery = (
        select(func.sum(dish_subquery))
        .where(Submenu.menu_id == Menu.id)
        .correlate(Menu)
        .label("dishCount")
    )



"""

Обработка и добавление новых параметров в словарь

"""


async def is_title_unique(session, title, model):
    # Создаем SELECT-запрос, чтобы проверить уникальность значения title
    query = select(model).where(model.title == title)

    # Выполняем запрос на выборку
    result = await session.execute(query)

    # Получаем результат запроса
    row = result.fetchone()

    # Если результат не пустой, значит значение title уже существует в таблице
    return row is None


def counter_menu(i):
    obj = jsonable_encoder( i[0] )
    obj['submenus_count']  = i[1]

    if i[2]:
        obj['dishes_count']  = int(i[2])
        return obj
    
    obj['dishes_count']  = 0
    return obj


def counter_submenu(i):
    obj = jsonable_encoder( i[0] )
    obj['dishes_count']  = i[1]
    return obj


def price_rounding(row):

    dish = jsonable_encoder(row[0])

    try:
        price_float = float(dish['price'])
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid price format. Price must be a number.")
    
    rounded_price = round(price_float, 2)
    dish['price'] = "{:.2f}".format(rounded_price)

    return dish



'''

Запросы в базу Menu

'''



async def get_specific_menu_db( session: AsyncSession, menu_id ):
    
    query = select(Menu, submenu_subquery, sub_dish_subquery).where( Menu.id == menu_id )


    result = await session.execute( query )
    row = result.first()

    if not row:
        raise HTTPException( status_code=404, detail="menu not found" )
    
    specific_menu = counter_menu(row)

    return specific_menu




async def get_all_menu_db( session : AsyncSession ):

    query = select(Menu, submenu_subquery, sub_dish_subquery)

    result = await session.execute( query )

    menus_list = result.all()
    menus_dict_list = [ counter_menu(menu) for menu in menus_list ]

    return menus_dict_list




    
async def create_menu_db( session: AsyncSession, new_menu ):

    if not await is_title_unique(session, new_menu.model_dump()['title'], Menu):
        raise HTTPException( status_code=404, detail="the menu already exists" )
    
    stmt = insert( Menu ).values(**new_menu.model_dump())
    result = await session.execute(stmt)
    new_menu_id = result.inserted_primary_key[0]
    await session.commit()

    specific_menu = await get_specific_menu_db(session, new_menu_id)

    return specific_menu




async def update_menu_db( session: AsyncSession, updated_menu, menu_id ):

    stmt = update(Menu).values(**updated_menu.model_dump()).where(Menu.id == menu_id) 
    await session.execute(stmt)

    await session.commit()

    updated_menu = await get_specific_menu_db(session, menu_id)

    return updated_menu




async def delete_menu_db(session: AsyncSession, menu_id ):

    stmt = delete(Menu).where(Menu.id == menu_id)
    result = await session.execute(stmt)
    await session.commit()
    

    return  { "status": 'true', "message": "The menu has been deleted"}













'''

Запросы в базу Submenu

'''


async def get_all_submenu_db(session: AsyncSession, menu_id):

    query = select(Submenu, dish_subquery ).where(Submenu.menu_id == menu_id)
    result = await session.execute(query)
    submenus_list = result.all()

    submenus = [counter_submenu(submenu) for submenu in submenus_list]
    return submenus



async def get_specific_submenu_db(session: AsyncSession, menu_id, submenu_id):

    query = select(Submenu, dish_subquery).where(and_(Submenu.id == submenu_id, Submenu.menu_id == menu_id) )
    result = await session.execute(query)
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="submenu not found")
    specific_submenu = counter_submenu(row)

    return specific_submenu



async def create_submenu_db(session, subnew_menu, menu_id):

    if not await is_title_unique(session, subnew_menu.model_dump()['title'], Submenu):
        raise HTTPException( status_code=404, detail="the submenu already exists" )
    
    stmt = insert(Submenu).values(**subnew_menu.model_dump(), menu_id=menu_id)
    result = await session.execute(stmt)

    new_submenu_id = result.inserted_primary_key[0]
    await session.commit()

    specific_submenu = await get_specific_submenu_db(session, menu_id, new_submenu_id)

    return specific_submenu


async def update_submenu_db(session, updated_submenu, menu_id, submenu_id):

    stmt = update(Submenu).values(**updated_submenu.model_dump()).where(and_(Submenu.id == submenu_id, Submenu.menu_id == menu_id) )
    await session.execute(stmt)

    await session.commit()

    updated_submenu = await get_specific_submenu_db(session, menu_id, submenu_id)

    return updated_submenu



async def delete_submenu_db(session: AsyncSession, menu_id, submenu_id ):

    stmt = delete(Submenu).where(and_(Submenu.id == submenu_id, Submenu.menu_id == menu_id) )
    await session.execute(stmt)
    await session.commit()

    return { "status": 'true', "message": "The submenu has been deleted"}








'''

Запросы в базу Dish

'''


async def get_all_dish_db(session: AsyncSession, menu_id, submenu_id):

    query = select(Dish).join( Submenu, Dish.submenu_id == submenu_id).where(Submenu.menu_id == menu_id)
    result = await session.execute(query)

    dishes_list = result.all()

    submenus = [price_rounding(dish) for dish in dishes_list]

    return submenus



async def get_specific_dish_db(session: AsyncSession, menu_id, submenu_id, dish_id):

    query = select(Dish).join( Submenu, Dish.submenu_id == submenu_id).where(and_(Submenu.menu_id == menu_id, Dish.id == dish_id))
    result = await session.execute(query)

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="dish not found")
    
    specific_dish = price_rounding(row) 

    return specific_dish



async def create_dish_db(session, dish_menu, menu_id, submenu_id):

    if not await is_title_unique(session, dish_menu.model_dump()['title'], Dish):
        raise HTTPException( status_code=404, detail="the dish already exists" )

    stmt = insert(Dish).values(**dish_menu.model_dump(), submenu_id=submenu_id)
    result = await session.execute(stmt)

    new_dish_id = result.inserted_primary_key[0]
    await session.commit()

    specific_dish = await get_specific_dish_db(session, menu_id, submenu_id, new_dish_id  )

    return specific_dish




async def update_dish_db(session, updated_dish, menu_id, submenu_id, dish_id):

    stmt = update(Dish).values(**updated_dish.model_dump()).where(and_(Dish.submenu_id == submenu_id, Dish.id == dish_id))

    await session.execute(stmt)

    await session.commit()

    updated_dish = await get_specific_dish_db(session, menu_id, submenu_id, dish_id)

    return updated_dish



async def delete_dish_db(session: AsyncSession, menu_id, submenu_id, dish_id):

    stmt = delete(Dish).where(and_(Dish.submenu_id == submenu_id, Dish.id == dish_id))
    await session.execute(stmt)
    await session.commit()

    return { "status": 'true', "message": "The dish has been deleted"}



