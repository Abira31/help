from pydantic import BaseModel
from datetime import datetime

class ResumesBase(BaseModel):
    id : int
    salary : int
    title : str
    description : str
    publication_date : datetime
    is_active : bool
    class Config:
        orm_mode = True

class ResumesSaveBase(BaseModel):
    salary : int
    title : str
    description : str
    class Config:
        orm_mode = True