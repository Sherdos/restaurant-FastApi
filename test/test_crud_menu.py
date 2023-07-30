from httpx import AsyncClient

menu_id = ''
menu_title = ''
menu_description = ''

async def test_get_list_menu_empty(ac: AsyncClient):
    result = await ac.get('/api/v1/menus/')
    assert result.status_code == 200
    assert len(result.json()) == 0

async def test_create_menu(ac: AsyncClient):

    global menu_id
    global menu_title
    global menu_description

    result = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    
    menu_id = result.json()['id']
    menu_title = result.json()['title']
    menu_description = result.json()['description']

    assert menu_id == result.json()['id']
    assert menu_title == result.json()['title']
    assert menu_description == result.json()['description']
    assert result.status_code == 201


async def test_get_list_menu(ac: AsyncClient):
    result = await ac.get('/api/v1/menus/')
    assert result.status_code == 200
    assert len(result.json()) == 1


async def test_get_specific_menu(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{menu_id}')
    assert result.status_code == 200

    assert menu_id == result.json()['id']
    assert menu_title == result.json()['title']
    assert menu_description == result.json()['description']


async def test_update_menu(ac: AsyncClient):

    global menu_title
    global menu_description

    result = await ac.patch(f'/api/v1/menus/{menu_id}', json={
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    })
    assert result.status_code == 200

    assert menu_title != result.json()['title']
    assert menu_description != result.json()['description']

    menu_title = result.json()['title']
    menu_description = result.json()['description']

    assert menu_title == result.json()['title']
    assert menu_description == result.json()['description']



async def test_delete_menu(ac: AsyncClient):

    result = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert result.status_code == 200




