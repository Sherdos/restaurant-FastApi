from httpx import AsyncClient


class TestMenu:

    def setup_class(self):
        self.submenu_id = ''
        self.submenu_title = ''
        self.submenu_description = ''
        self.submenu_menu_id = ''

    async def test_crud_submenu(self, ac: AsyncClient, menu_data, submenu_data, update_submenu_data):

        result_menu = await ac.post('/api/v1/menus/', json=menu_data)

        assert result_menu.status_code == 201
        self.submenu_menu_id = result_menu.json()['id']

        result = await ac.post(f'/api/v1/menus/{self.submenu_menu_id}/submenus', json=submenu_data)

        assert result.status_code == 201
        self.submenu_id = result.json()['id']
        self.submenu_title = result.json()['title']
        self.submenu_description = result.json()['description']

        result = await ac.get(f'/api/v1/menus/{self.submenu_menu_id}/submenus/{self.submenu_id}')
        assert result.status_code == 200

        assert self.submenu_id == result.json()['id']
        assert self.submenu_title == result.json()['title']
        assert self.submenu_description == result.json()['description']

        result = await ac.patch(f'/api/v1/menus/{self.submenu_menu_id}/submenus/{self.submenu_id}', json=update_submenu_data)
        assert result.status_code == 200

        assert self.submenu_title != result.json()['title']
        assert self.submenu_description != result.json()['description']

        self.submenu_title = result.json()['title']
        self.submenu_description = result.json()['description']

        result = await ac.delete(f'/api/v1/menus/{self.submenu_menu_id}/submenus/{self.submenu_id}')
        assert result.status_code == 200

        result = await ac.get(f'/api/v1/menus/{self.submenu_menu_id}/submenus')
        assert result.status_code == 200
        assert len(result.json()) == 0

        await ac.delete(f'/api/v1/menus/{self.submenu_menu_id}')
