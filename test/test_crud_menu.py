from httpx import AsyncClient


class TestMenu:
    def setup_class(self):
        self.id = None
        self.title = None
        self.description = None

    async def test_crud_menu(self, ac: AsyncClient, menu_data, update_menu_data):

        menu_list = await ac.get('/api/v1/menus/')
        assert menu_list.status_code == 200
        assert menu_list.json() == []

        result = await ac.post('/api/v1/menus/', json=menu_data)
        assert result.status_code == 201
        self.id = result.json()['id']

        self.title = result.json()['title']
        self.description = result.json()['description']

        menu = await ac.get(f'/api/v1/menus/{self.id}')
        assert menu.status_code == 200
        assert self.title == menu.json()['title']
        assert self.description == menu.json()['description']

        result = await ac.patch(f'/api/v1/menus/{self.id}', json=update_menu_data)
        assert result.status_code == 200
        assert self.title != result.json()['title']
        assert self.description != result.json()['description']

        self.title = result.json()['title']
        self.description = result.json()['description']

        result = await ac.delete(f'/api/v1/menus/{self.id}')
        assert result.status_code == 200

        menu_list = await ac.get('/api/v1/menus/')
        assert menu_list.status_code == 200
        assert menu_list.json() == []
