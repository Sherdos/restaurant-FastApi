from httpx import AsyncClient



menu_id = ''
submenu_id = ''

async def test_create_all_object(ac: AsyncClient):

    global menu_id
    global submenu_id

    result_menu = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    
    menu_id = result_menu.json()['id']

    result_submenu = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    
    submenu_id = result_submenu.json()['id']

    await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })

    await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json={
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50"
    })



async def test_get_specific_menu(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{menu_id}')

    assert result.status_code == 200
    assert menu_id == result.json()['id']
    assert 1 == result.json()['submenus_count']
    assert 2 == result.json()['dishes_count']



async def test_get_specific_submenu(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')

    assert result.status_code == 200
    assert submenu_id == result.json()['id']
    assert 2 == result.json()['dishes_count']



async def test_delete_submenu(ac: AsyncClient):

    result = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert result.status_code == 200


async def test_get_list_submenu(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{menu_id}/submenus')
    assert result.status_code == 200
    assert len(result.json()) == 0


async def test_get_list_dish(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert result.status_code == 200
    assert len(result.json()) == 0


async def test_get_specific_menu_empty(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{menu_id}')

    assert result.status_code == 200

    assert menu_id == result.json()['id']
    assert 0 == result.json()['submenus_count']
    assert 0 == result.json()['dishes_count']


async def test_delete_menu(ac: AsyncClient):

    result = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert result.status_code == 200


async def test_get_list_menu(ac: AsyncClient):

    result = await ac.get('/api/v1/menus/')
    assert result.status_code == 200
    assert len(result.json()) == 0