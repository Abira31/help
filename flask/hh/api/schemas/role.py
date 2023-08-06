from pydantic import BaseModel

class RolesBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class RoleDetailBase(BaseModel):
    name: str
    class Config:
        orm_mode = True



