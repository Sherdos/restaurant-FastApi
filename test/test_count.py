from httpx import AsyncClient

class TestCountingSubmenusAndDishes:

    def setup_class(self):
        self.menu_id = ''
        self.submenu_id = ''




    async def test_count(self, ac: AsyncClient, menu_data:dict, submenu_data:dict, dish_data:dict) -> None:

        result_menu = await ac.post('/api/v1/menus', json=menu_data)
        assert result_menu.status_code == 201
        self.menu_id = result_menu.json()['id']

        result_submenu = await ac.post(f'/api/v1/menus/{self.menu_id}/submenus', json=submenu_data)
        assert result_submenu.status_code == 201
        self.submenu_id = result_submenu.json()['id']

        result_dish = await ac.post(f'/api/v1/menus/{self.menu_id}/submenus/{self.submenu_id}/dishes', json=dish_data)
        assert result_dish.status_code == 201

        menu = await ac.get(f'/api/v1/menus/{self.menu_id}')
        assert menu.status_code == 200
        assert self.menu_id == menu.json()['id']
        assert 1 == menu.json()['dishes_count']
        assert 1 == menu.json()['submenus_count']

        submenu = await ac.get(f'/api/v1/menus/{self.menu_id}/submenus/{self.submenu_id}')
        assert submenu.status_code == 200
        assert self.submenu_id == submenu.json()['id']
        assert 1 == submenu.json()['dishes_count']


        delete_submenu = await ac.delete(f'/api/v1/menus/{self.menu_id}/submenus/{self.submenu_id}')
        assert delete_submenu.status_code == 200

        submenu_list = await ac.get(f'/api/v1/menus/{self.menu_id}/submenus')
        assert submenu_list.status_code == 200
        assert len(submenu_list.json()) == 0

        dish_list = await ac.get(f'/api/v1/menus/{self.menu_id}/submenus/{self.submenu_id}/dishes')
        assert dish_list.status_code == 200
        assert len(dish_list.json()) == 0

        menu = await ac.get(f'/api/v1/menus/{self.menu_id}')
        assert menu.status_code == 200
        assert self.menu_id == menu.json()['id']
        assert 0 == menu.json()['submenus_count']
        assert 0 == menu.json()['dishes_count']


        delete_menu = await ac.delete(f'/api/v1/menus/{self.menu_id}')
        assert delete_menu.status_code == 200


        empty_list = await ac.get('/api/v1/menus')
        assert empty_list.status_code == 200
        assert len(empty_list.json()) == 0