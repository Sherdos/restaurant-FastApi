from httpx import AsyncClient

dish_id = ''
dish_title = ''
dish_description = ''
dish_price = ''
dish_submenu_id = ''
dish_submenu_menu_id = ''


async def test_create_dish(ac: AsyncClient):

    global dish_id
    global dish_title
    global dish_description
    global dish_submenu_id
    global dish_price
    global dish_submenu_menu_id

    result_menu = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    dish_submenu_menu_id = result_menu.json()['id']

    result_submenu = await ac.post(f'/api/v1/menus/{dish_submenu_menu_id}/submenus', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })

    dish_submenu_id = result_submenu.json()['id']

    result = await ac.post(f'/api/v1/menus/{dish_submenu_menu_id}/submenus/{dish_submenu_id}/dishes', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })

    dish_id = result.json()['id']
    dish_title = result.json()['title']
    dish_description = result.json()['description']
    dish_price = result.json()['price']

    assert dish_id == result.json()['id']
    assert dish_title == result.json()['title']
    assert dish_description == result.json()['description']
    assert dish_price == result.json()['price']
    assert result.status_code == 201


async def test_get_list_dish(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{dish_submenu_menu_id}/submenus/{dish_submenu_id}/dishes')
    assert result.status_code == 200
    assert len(result.json()) == 1


async def test_get_specific_dish(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{dish_submenu_menu_id}/submenus/{dish_submenu_id}/dishes/{dish_id}')
    assert result.status_code == 200

    assert dish_id == result.json()['id']
    assert dish_title == result.json()['title']
    assert dish_description == result.json()['description']
    assert dish_price == result.json()['price']


async def test_update_dish(ac: AsyncClient):

    global dish_title
    global dish_description
    global dish_price

    result = await ac.patch(f'/api/v1/menus/{dish_submenu_menu_id}/submenus/{dish_submenu_id}/dishes/{dish_id}', json={
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
        "price":"14.22"
    })
    assert result.status_code == 200

    assert dish_title != result.json()['title']
    assert dish_description != result.json()['description']
    assert dish_price != result.json()['price']

    dish_title = result.json()['title']
    dish_description = result.json()['description']
    dish_price = result.json()['price']

    assert dish_title == result.json()['title']
    assert dish_description == result.json()['description']
    assert dish_price == result.json()['price']



async def test_delete_dish(ac: AsyncClient):

    result = await ac.delete(f'/api/v1/menus/{dish_submenu_menu_id}/submenus/{dish_submenu_id}/dishes/{dish_id}')
    assert result.status_code == 200




