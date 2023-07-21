



from pydantic import BaseModel, Field


class Menu(BaseModel):
    # id:int
    title:str = Field(max_length=25)
    description:str
