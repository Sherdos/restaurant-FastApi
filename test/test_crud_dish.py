from httpx import AsyncClient


class TestMenu:

    def setup_class(self):
        self.dish_id = ''
        self.dish_title = ''
        self.dish_description = ''
        self.dish_price = ''
        self.dish_submenu_id = ''
        self.dish_submenu_menu_id = ''

    async def test_crud_submenu(self, ac: AsyncClient, menu_data, submenu_data, dish_data, update_dish_data):

        result_menu = await ac.post('/api/v1/menus/', json=menu_data)
        self.dish_submenu_menu_id = result_menu.json()['id']

        result_submenu = await ac.post(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus', json=submenu_data)
        self.dish_submenu_id = result_submenu.json()['id']

        result = await ac.post(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes', json=dish_data)

        assert result.status_code == 201
        self.dish_id = result.json()['id']
        self.dish_title = result.json()['title']
        self.dish_description = result.json()['description']
        self.dish_price = result.json()['price']

        result = await ac.get(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes/{self.dish_id}')
        assert result.status_code == 200
        assert self.dish_id == result.json()['id']
        assert self.dish_title == result.json()['title']
        assert self.dish_description == result.json()['description']
        assert self.dish_price == result.json()['price']

        result = await ac.patch(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes/{self.dish_id}', json=update_dish_data)
        assert result.status_code == 200

        assert self.dish_title != result.json()['title']
        assert self.dish_description != result.json()['description']
        assert self.dish_price != result.json()['price']

        self.dish_title = result.json()['title']
        self.dish_description = result.json()['description']
        self.dish_price = result.json()['price']

        result = await ac.delete(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes/{self.dish_id}')
        assert result.status_code == 200

        result = await ac.get(f'/api/v1/menus/{self.dish_submenu_menu_id}/submenus/{self.dish_submenu_id}/dishes')
        assert result.status_code == 200
        assert len(result.json()) == 0

        await ac.delete(f'/api/v1/menus/{self.dish_submenu_menu_id}')
