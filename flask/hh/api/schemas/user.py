from pydantic import BaseModel
from api.schemas.role import RolesBase
from api.schemas.resumes import ResumesBase
class UserBase(BaseModel):
    email : str
    password : str
    first_name : str
    last_name : str
    phone : str
    class Config:
        orm_mode = True


class UserDetailBase(UserBase):
    id : int
    is_active : bool
    roles : list[RolesBase]
    is_admin: bool


