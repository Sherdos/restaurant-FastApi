from httpx import AsyncClient


class TestSubmenu:

    def setup_class(self):
        self.submenu_id = None
        self.submenu_title = None
        self.submenu_description = None
        self.submenu_menu_id = None

    async def test_create_submenu(self, ac: AsyncClient, menu_data, submenu_data):
        result_menu = await ac.post('/api/v1/menus', json=menu_data)

        assert result_menu.status_code == 201
        self.__class__.submenu_menu_id = result_menu.json()['id']

        result = await ac.post(f'/api/v1/menus/{self.submenu_menu_id}/submenus', json=submenu_data)

        assert result.status_code == 201
        self.__class__.submenu_id = result.json()['id']
        self.__class__.submenu_title = result.json()['title']
        self.__class__.submenu_description = result.json()['description']

    async def test_get_submenu(self, ac: AsyncClient):
        result = await ac.get(f'/api/v1/menus/{self.submenu_menu_id}/submenus/{self.submenu_id}')
        assert result.status_code == 200
        assert self.submenu_id == result.json()['id']
        assert self.submenu_title == result.json()['title']
        assert self.submenu_description == result.json()['description']

    async def test_update_submenu(self, ac: AsyncClient, update_submenu_data):

        result = await ac.patch(f'/api/v1/menus/{self.submenu_menu_id}/submenus/{self.submenu_id}', json=update_submenu_data)
        assert result.status_code == 200

        assert self.submenu_title != result.json()['title']
        assert self.submenu_description != result.json()['description']

        self.__class__.submenu_title = result.json()['title']
        self.__class__.submenu_description = result.json()['description']

    async def test_delete_submenu(self, ac: AsyncClient):
        result = await ac.delete(f'/api/v1/menus/{self.submenu_menu_id}/submenus/{self.submenu_id}')
        assert result.status_code == 200

    async def test_empty_submenu_list_and_clean(self, ac: AsyncClient, ):
        result = await ac.get(f'/api/v1/menus/{self.submenu_menu_id}/submenus')
        assert result.status_code == 200
        assert len(result.json()) == 0

        result = await ac.delete(f'/api/v1/menus/{self.submenu_menu_id}')
        assert result.status_code == 200
