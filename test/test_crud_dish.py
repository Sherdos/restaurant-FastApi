from httpx import AsyncClient


class TestDish:

    def setup_class(self):
        self.dish_id = None
        self.dish_title = None
        self.dish_description = None
        self.dish_price = None
        self.dish_submenu_id = None
        self.dish_submenu_menu_id = None

    async def test_create_dish(self, ac:AsyncClient, menu_data, submenu_data, dish_data):
        result_menu = await ac.post('/api/v1/menus', json=menu_data)
        self.__class__.dish_submenu_menu_id = result_menu.json()['id']

        result_submenu = await ac.post(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus', json=submenu_data)
        self.__class__.dish_submenu_id = result_submenu.json()['id']

        result = await ac.post(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes', json=dish_data)

        assert result.status_code == 201
        self.__class__.dish_id = result.json()['id']
        self.__class__.dish_title = result.json()['title']
        self.__class__.dish_description = result.json()['description']
        self.__class__.dish_price = result.json()['price']

    async def test_get_dish(self, ac:AsyncClient):

        result = await ac.get(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes/{self.dish_id}')
        assert result.status_code == 200
        assert self.dish_id == result.json()['id']
        assert self.dish_title == result.json()['title']
        assert self.dish_description == result.json()['description']
        assert self.dish_price == result.json()['price']

    async def test_update_dish(self, ac:AsyncClient, update_dish_data):
        result = await ac.patch(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes/{self.dish_id}', json=update_dish_data)
        assert result.status_code == 200

        assert self.dish_title != result.json()['title']
        assert self.dish_description != result.json()['description']
        assert self.dish_price != result.json()['price']

        self.dish_title = result.json()['title']
        self.dish_description = result.json()['description']
        self.dish_price = result.json()['price']

    async def test_delete_dish(self, ac:AsyncClient):
        result = await ac.delete(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes/{self.dish_id}')
        assert result.status_code == 200

    async def test_empty_dish_list_and_clean(self, ac:AsyncClient):
        result = await ac.get(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes')
        assert result.status_code == 200
        assert len(result.json()) == 0

        result = await ac.delete(f'/api/v1/menus/{self.dish_submenu_menu_id}')
        assert result.status_code == 200

