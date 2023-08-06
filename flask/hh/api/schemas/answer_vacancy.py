from pydantic import BaseModel

class AnswerVacancyBaseModel(BaseModel):
    user_resume : int
    vacancy : int