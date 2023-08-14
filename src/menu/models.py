import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship

from src.menu.schemas import AllDish, AllMenu, AllSubmenu, GetDish, GetMenu, GetSubmenu


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)

    submenus = relationship('Submenu', back_populates='parent')

    def json_mapping(self, item: tuple) -> GetMenu:
        return GetMenu(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus_count=item[-2],
            dishes_count=item[-1]
        )

    def json_mapping_all(self) -> AllMenu:
        return AllMenu(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus=[
                AllSubmenu(
                    id=submenu.id,
                    title=submenu.title,
                    description=submenu.description,
                    dishes=[
                        AllDish(
                            id=dish.id,
                            title=dish.title,
                            description=dish.description,
                            price=dish.price
                        ) for dish in submenu.dishes
                    ]
                ) for submenu in self.submenus
            ],
        )


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))
    dishes = relationship('Dish', back_populates='parent')
    parent = relationship('Menu', back_populates='submenus')

    def json_mapping(self, item: tuple) -> GetSubmenu:
        return GetSubmenu(
            id=self.id,
            title=self.title,
            description=self.description,
            menu_id=self.menu_id,
            dishes_count=item[-1]
        )


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'))
    parent = relationship('Submenu', back_populates='dishes')

    def json_mapping(self, item=None) -> GetDish:
        return GetDish(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price,
            submenu_id=self.submenu_id
        )
