
from sqlalchemy import String, ForeignKey, Column, UUID
import uuid
from sqlalchemy.orm import DeclarativeBase

from src.menu.schemas import GetDish, GetMenu, GetSubmenu


class Base(DeclarativeBase):
    pass

class Menu(Base):
    __tablename__ = "menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)

    @staticmethod
    def json_mapping(item):
        menu = item[0]
        return GetMenu(
                    id=menu.id, 
                    title=menu.title, 
                    description=menu.description, 
                    submenus_count=item[-2], 
                    dishes_count=item[-1]
                ) 


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))

    @staticmethod
    def json_mapping(item):
        submenu:Submenu = item[0]
        return GetSubmenu(
                    id=submenu.id, 
                    title=submenu.title, 
                    description=submenu.description, 
                    menu_id=submenu.menu_id,
                    dishes_count=item[-1]
                ) 



class Dish(Base):
    __tablename__ = "dish"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'))

    @staticmethod
    def json_mapping(item):
        dish:Dish = item[0]
        return GetDish(
                    id=dish.id, 
                    title=dish.title, 
                    description=dish.description, 
                    price=dish.price,
                    submenu_id=dish.submenu_id
                ) 

        
