import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase

from src.menu.schemas import GetDish, GetMenu, GetSubmenu


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)

    def json_mapping(self, item: tuple) -> GetMenu:
        return GetMenu(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus_count=item[-2],
            dishes_count=item[-1]
        )


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))

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

    def json_mapping(self, item=None) -> GetDish:
        return GetDish(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price,
            submenu_id=self.submenu_id
        )
