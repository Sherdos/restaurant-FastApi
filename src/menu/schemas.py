from uuid import UUID

from pydantic import BaseModel, Field

'''

Get

'''


class Base(BaseModel):

    title: str = Field(max_length=25)
    description: str


class BaseGet(Base):
    id: UUID


class GetMenu(BaseGet):
    submenus_count: int
    dishes_count: int


class GetSubmenu(BaseGet):
    menu_id: UUID
    dishes_count: int


class GetDish(BaseGet):
    price: str
    submenu_id: UUID


'''

Create

'''


class CreateMenu(Base):
    pass


class CreateDish(Base):
    price: str


'''

ALL

'''


class AllDish(BaseGet):
    price: str


class AllSubmenu(BaseGet):
    dishes: list[AllDish]


class AllMenu(BaseGet):
    submenus: list[AllSubmenu]
