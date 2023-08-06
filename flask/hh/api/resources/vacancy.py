from flask_restful import Resource
from api.models import Vacancy,Сompany,Resume,User
from api import db
from flask import jsonify,request,make_response
from api.schemas.vacancy import VacancyBase,VacancyDetailBase
from api.schemas.answer_vacancy import AnswerVacancyBaseModel
from pydantic import ValidationError
from flask_jwt_extended import jwt_required,current_user
from api.core.permission import is_user_company,has_permission_obj_user_company
from sqlalchemy.orm import join

class VacancyAPI(Resource):
    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def get(self,id=None):
        if not id:
            vacancy_db = current_user.company.vacancy.all()
            vacancy = [VacancyDetailBase.from_orm(vacancy) for vacancy in vacancy_db]
            response = make_response(
                jsonify([v.dict() for v in vacancy]),
            200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        vacancy_db = db.session.query(Vacancy).select_from(join(Vacancy, Сompany, Сompany.vacancy)).filter(Vacancy.id == id).first()
        if not vacancy_db:
            return [],204
        vacancy = VacancyDetailBase.from_orm(vacancy_db)
        response = make_response(
            jsonify(vacancy.dict()),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def post(self):
        try:
            vacancy = VacancyBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(),400
            )
            response.headers["Content-Type"] = "application/json"
            return response
        vacancy_db = Vacancy(**vacancy.dict())
        vacancy_db.company_id = current_user.company.id
        db.session.add(vacancy_db)
        db.session.commit()
        vacancy = VacancyDetailBase.from_orm(vacancy_db)
        response = make_response(
            jsonify(vacancy.dict()),
            201
        )
        response.headers["Content-Type"] = "application/json"
        return response
    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def put(self,id):
        vacancy_db = db.session.query(Vacancy).select_from(join(Vacancy, Сompany, Сompany.vacancy)).filter(Vacancy.id == id).first()
        if not vacancy_db:
            return [],204
        try:
            vacancy = VacancyBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(),400
            )
            response.headers["Content-Type"] = "application/json"
            return response

        for key, value in vacancy.dict().items():
            setattr(vacancy_db, key, value)

        db.session.add(vacancy_db)
        db.session.commit()
        vacancy = VacancyDetailBase.from_orm(vacancy_db)
        response = make_response(
            jsonify(vacancy.dict()),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def delete(self,id):
        vacancy_db = db.session.query(Vacancy).select_from(join(Vacancy, Сompany, Сompany.vacancy)).filter(Vacancy.id == id).first()
        if not vacancy_db:
            return [],204
        db.session.delete(vacancy_db)
        db.session.commit()
        return [],204

class SearchVacancyAPI(Resource):
    @jwt_required()
    def get(self,id=None):
        if not id:
            vacancys_db = db.session.query(Vacancy).select_from(join(Vacancy, Сompany, Сompany.vacancy)).\
                filter(Vacancy.is_active == True).all()
            vacancy = [VacancyDetailBase.from_orm(vacancy) for vacancy in vacancys_db]
            response = make_response(
                jsonify([v.dict() for v in vacancy]),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        vacancy_db = db.session.query(Vacancy).select_from(join(Vacancy, Сompany, Сompany.vacancy)).\
            filter(Vacancy.id == id,Vacancy.is_active).first()
        if not vacancy_db:
            return [],204
        vacancy = VacancyDetailBase.from_orm(vacancy_db)
        response = make_response(
            jsonify(vacancy.dict()),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response

class AnswerVacancyAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            answer = AnswerVacancyBaseModel.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(),400
            )
            response.headers["Content-Type"] = "application/json"
            return response
        vacancy_db = db.session.query(Vacancy).select_from(join(Vacancy, Сompany, Сompany.vacancy)). \
            filter(Vacancy.id == answer.vacancy, Vacancy.is_active).first()
        resume_db = db.session.query(Resume).select_from(join(Resume, User, User.resumes)).filter(Resume.id == answer.user_resume,
                                                                                                  User.id == current_user.id).first()
        vacancy_resume = db.session.query(Vacancy).select_from(join(Vacancy, Resume, Vacancy.resumes)). \
            filter(Vacancy.id == vacancy_db.id, Resume.id == resume_db.id).first()
        if vacancy_resume is None:
            vacancy_db.resumes.append(resume_db)
            db.session.add(vacancy_db)
            db.session.commit()
            response = make_response(
                jsonify(msg="Отклик отправлен"), 201
            )
            response.headers["Content-Type"] = "application/json"
            return response
        response = make_response(
            jsonify(msg="Вы уже откликнулись"), 200
        )
        response.headers["Content-Type"] = "application/json"
        return response



        