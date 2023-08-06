from api.models import Role,Vacancy,Skills
from api import db
from abc import ABC,abstractmethod
from api.core.fale_data import roles,vacancys,skills

class CreateFakeDataABC(ABC):
    roles = []
    vacancys = []
    skills = []
    @classmethod
    @abstractmethod
    def create(cls):
        pass

class CreateFakeDataRoles(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for r in roles:
            rol = Role(**r)
            db.session.add(rol)
            db.session.commit()
            cls.roles.append(rol)

class CreateFakeDataVacancys(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for v in vacancys:
            vac = Vacancy(**v)
            db.session.add(vac)
            db.session.commit()
            cls.vacancys.append(vac)
    
class CreateFakeDataSkills(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for s in skills:
            sk = Skills(**s)
            db.session.add(sk)
            db.session.commit()
            cls.skills.append(sk)


class CreateFakeData(CreateFakeDataABC):
    @classmethod
    def create(cls):
        db.session.query(Role).delete()
        db.session.query(Vacancy).delete()
        db.session.query(Skills).delete()
        db.session.commit()

        CreateFakeDataRoles.create()
        # CreateFakeDataVacancys.create()
        CreateFakeDataSkills.create()







    