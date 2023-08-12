from httpx import AsyncClient


class TestMenu:

    def setup_class(self):
        self.id = None
        self.title = None
        self.description = None



    async def test_create_menu(self, ac: AsyncClient, menu_data):
        result = await ac.post('/api/v1/menus', json=menu_data)
        assert result.status_code == 201
        self.__class__.id = result.json()['id']
        self.__class__.title = result.json()['title']
        self.__class__.description = result.json()['description']


    async def test_get_menu(self, ac: AsyncClient):
        menu = await ac.get(f'/api/v1/menus/{self.__class__.id}')
        assert menu.status_code == 200
        assert self.__class__.title == menu.json()['title']
        assert self.__class__.description == menu.json()['description']


    async def test_update_menu(self, ac: AsyncClient, update_menu_data):
        result = await ac.patch(f'/api/v1/menus/{self.__class__.id}', json=update_menu_data)
        assert result.status_code == 200
        assert self.__class__.title != result.json()['title']
        assert self.__class__.description != result.json()['description']

        self.__class__.title = result.json()['title']
        self.__class__.description = result.json()['description']


    async def test_delete_menu(self, ac: AsyncClient):
        result = await ac.delete(f'/api/v1/menus/{self.__class__.id}')
        assert result.status_code == 200


    async def test_get_all_menus(self, ac: AsyncClient):
        menu_list = await ac.get('/api/v1/menus')
        assert menu_list.status_code == 200
        assert menu_list.json() == []




