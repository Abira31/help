from pydantic import BaseModel
from api.schemas.resumes import ResumesSaveBase
class VacancyBase(BaseModel):
    name: str
    description : str
    class Config:
        orm_mode = True

class VacancyDetailBase(VacancyBase):
   id : int


