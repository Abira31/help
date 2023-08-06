import datetime

from . import db
from werkzeug.security import generate_password_hash

from api import jwt
import pytz

UTC = pytz.utc
IST = pytz.timezone('Asia/Yekaterinburg')

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

job_skills = db.Table(
    'job_skills',
    db.Column('skills_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True),
    db.Column('resume_id', db.Integer, db.ForeignKey('resume.id'), primary_key=True)
)
user_resumes = db.Table(
    'user_resumes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('resume_id', db.Integer, db.ForeignKey('resume.id'), primary_key=True)
)

vacancy_resumes = db.Table(
    'vacancy_resumes',
    db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id'), primary_key=True),
    db.Column('resume_id', db.Integer, db.ForeignKey('resume.id'), primary_key=True)
)

class Сompany(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_active = db.Column(db.Boolean(), nullable=False)
    user = db.relationship("User",backref="company",lazy='dynamic')
    vacancy = db.relationship("Vacancy",backref="company",lazy='dynamic')

    def __init__(self,name,description,email,is_active=True,vacancy=None):
        self.name = name
        self.description = description
        self.email = email
        self.is_active = is_active
        if not vacancy:
            self.vacancy = []
        else:
            self.vacancy = vacancy



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),nullable=False,unique=True)
    password = db.Column(db.String(120),nullable=False)
    is_active = db.Column(db.Boolean(),nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    resumes = db.relationship('Resume', secondary=user_resumes, lazy='subquery', backref=db.backref('user_resumes', lazy=True))
    roles = db.relationship('Role', secondary=roles_users, lazy='subquery', backref=db.backref('user_roles', lazy=True))
    is_admin = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    def __init__(self,email,password,first_name,last_name,phone,is_active=True,resumes=None,roles=None,is_admin=False,company=None):
        self.email = email
        self.password = generate_password_hash(password)
        self.is_active = is_active
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        if not resumes:
            self.resumes = []
        else:
            self.resumes = resumes
        if not roles:
            self.roles = []
        else:
            self.roles = roles
        self.is_admin = is_admin
        if not company:
            self.company = None
        else:
            self.company = company

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)




class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    resumes = db.relationship('Resume', secondary=vacancy_resumes, lazy='subquery',backref=db.backref('vacancy_resume', lazy=True))
    is_active = db.Column(db.Boolean(), nullable=False)
    publication_date = db.Column(db.DateTime(timezone=True))
    company_id = db.Column(db.Integer,db.ForeignKey("company.id"))

    def __init__(self,name,description,resumes=None,is_active=True,publication_date=datetime.datetime.now(IST)):
        self.name = name
        self.description = description
        if not resumes:
            self.resumes = []
        else:
            self.resumes = resumes
        self.is_active = is_active
        self.publication_date = publication_date






class Skills(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer(),nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    skills = db.relationship('Skills', secondary=job_skills, lazy='subquery', backref=db.backref('resume_skills', lazy=True))
    publication_date = db.Column(db.DateTime(timezone=True))
    is_active = db.Column(db.Boolean(), nullable=False)

    def __init__(self,salary,title,description,skills=None,publication_date=datetime.datetime.now(IST),is_active=True):
        self.salary = salary
        self.title = title
        self.description = description
        if not skills:
            self.skills = []
        else:
            self.skills = skills
        self.publication_date = publication_date
        self.is_active = is_active






@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.query(User).filter_by(email=identity).first()