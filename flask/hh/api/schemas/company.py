from pydantic import BaseModel

class СompanyBaseModel(BaseModel):
    name : str
    description : str
    email : str
    class Config:
        orm_mode = True

class СompanyDetailBaseModel(СompanyBaseModel):
    id : int


