



from pydantic import BaseModel, Field



'''

Get

'''

class GetMenu(BaseModel):
    id:str
    title:str = Field(max_length=25)
    description:str
    submenus_count:int
    dishes_count:int

class GetSubmenu(BaseModel):
    id:str
    title:str = Field(max_length=25)
    description:str
    menu_id:str
    dishes_count:int

class GetDish(BaseModel):
    id:str
    title:str = Field(max_length=25)
    description:str
    price:str
    sub_menu:str



'''

Create

'''

class CreateMenu(BaseModel):
    title:str = Field(max_length=25)
    description:str


class CreateDish(BaseModel):
    title:str = Field(max_length=25)
    description:str
    price:str

