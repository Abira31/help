from pydantic import BaseModel

class SkillsBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class SkillsDetailBase(BaseModel):
    name: str
    class Config:
        orm_mode = True