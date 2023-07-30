from httpx import AsyncClient

submenu_id = ''
submenu_title = ''
submenu_description = ''
submenu_menu_id = ''


async def test_create_submenu(ac: AsyncClient):

    global submenu_id
    global submenu_title
    global submenu_description
    global submenu_menu_id

    result_menu = await ac.post('/api/v1/menus/', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })

    submenu_menu_id = result_menu.json()['id']

    result = await ac.post(f'/api/v1/menus/{submenu_menu_id}/submenus', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })

    submenu_id = result.json()['id']
    submenu_title = result.json()['title']
    submenu_description = result.json()['description']

    assert submenu_id == result.json()['id']
    assert submenu_title == result.json()['title']
    assert submenu_description == result.json()['description']
    assert result.status_code == 201


async def test_get_list_submenu(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{submenu_menu_id}/submenus')
    assert result.status_code == 200
    assert len(result.json()) == 1


async def test_get_specific_submenu(ac: AsyncClient):
    result = await ac.get(f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}')
    assert result.status_code == 200

    assert submenu_id == result.json()['id']
    assert submenu_title == result.json()['title']
    assert submenu_description == result.json()['description']


async def test_update_submenu(ac: AsyncClient):

    global submenu_title
    global submenu_description

    result = await ac.patch(f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}', json={
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    })
    assert result.status_code == 200

    assert submenu_title != result.json()['title']
    assert submenu_description != result.json()['description']

    submenu_title = result.json()['title']
    submenu_description = result.json()['description']

    assert submenu_title == result.json()['title']
    assert submenu_description == result.json()['description']



async def test_delete_submenu(ac: AsyncClient):

    result = await ac.delete(f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}')
    assert result.status_code == 200


async def test_delete_all(ac: AsyncClient):
    await ac.delete(f'/api/v1/menus/{submenu_menu_id}')

