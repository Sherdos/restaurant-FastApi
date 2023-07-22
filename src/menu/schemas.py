



from pydantic import BaseModel, Field


class CreateMenu(BaseModel):
    title:str = Field(max_length=25)
    description:str


class GetMenu(BaseModel):
    id:str
    title:str = Field(max_length=25)
    description:str
