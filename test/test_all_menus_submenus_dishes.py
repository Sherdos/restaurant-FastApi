from httpx import AsyncClient


class TestAllMenusSubmenusDishes:

    def setup_class(self):
        self.submenu_id = None
        self.menu_id = None

    async def test_create_all_menus_submenus_dishes(self, ac:AsyncClient, menu_data, submenu_data, dish_data):
        result_menu = await ac.post('/api/v1/menus', json=menu_data)
        assert result_menu.status_code == 201
        self.__class__.menu_id = result_menu.json()['id']

        result_submenu = await ac.post(f'/api/v1/menus/{self.menu_id}/submenus', json=submenu_data)
        assert result_submenu.status_code == 201
        self.__class__.submenu_id = result_submenu.json()['id']

        result = await ac.post(f'/api/v1/menus/{self.menu_id}/submenus/{self.submenu_id}/dishes', json=dish_data)

        assert result.status_code == 201

    async def test_get_all_menus_submenus_dishes(self, ac:AsyncClient):

        result = await ac.get(f'/api/v1/menus/all')
        assert result.status_code == 200
        assert len(result.json()) == 1
        assert len(result.json()[0]['submenus']) == 1
        assert len(result.json()[0]['submenus'][0]['dishes']) == 1
    


    async def test_delete_all_submenus_dishes(self, ac:AsyncClient):
        result = await ac.delete(f'/api/v1/menus/{self.menu_id}/submenus/{self.submenu_id}')
        assert result.status_code == 200

    async def test_get_all_menus_submenus(self, ac:AsyncClient):
        result = await ac.get(f'/api/v1/menus/all')
        assert result.status_code == 200
        assert len(result.json()) == 1
        assert len(result.json()[0]['submenus']) == 0

    
    async def test_delete_all_menus(self, ac:AsyncClient):
        result = await ac.delete(f'/api/v1/menus/{self.menu_id}')
        assert result.status_code == 200

    async def test_get_all_menus_empty(self, ac:AsyncClient):
        result = await ac.get(f'/api/v1/menus/all')
        assert result.status_code == 200
        assert len(result.json()) == 0