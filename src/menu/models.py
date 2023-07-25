
from sqlalchemy import String, ForeignKey, Column, UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Menu(Base):
    __tablename__ = "menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)



class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))


class Dish(Base):
    __tablename__ = "dish"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(30), unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'))


