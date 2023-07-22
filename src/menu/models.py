from sqlalchemy import MetaData, TIMESTAMP, Integer, String, Table, ForeignKey, Column

metadata = MetaData()


menu = Table(

    "menu",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("description", String),

)

submenu = Table(
    
    "submenu",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("menu_id", Integer, ForeignKey('menu.id', ondelete='CASCADE')),

)


dishe = Table(
    
    "dishe",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("price", String),
    Column("submenu_id", Integer, ForeignKey('submenu.id', ondelete='CASCADE')),

)