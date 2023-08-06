from flask_restful import Resource
from api.models import Сompany
from api import db
from flask import jsonify,request,make_response
from api.schemas.company import СompanyBaseModel,СompanyDetailBaseModel
from pydantic import ValidationError
from flask_jwt_extended import jwt_required,current_user
from api.core.permission import is_user_company,has_permission_obj_user_company

class СompanyAPI(Resource):
    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def get(self):
        company_db = current_user.company
        company = СompanyDetailBaseModel.from_orm(company_db)
        response = make_response(
            jsonify(company.dict()),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def put(self):
        company_db = current_user.company
        try:
            company = СompanyBaseModel.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(), 400,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        for key, value in company.dict().items():
            setattr(company_db, key, value)
        db.session.commit()
        db.session.refresh(company_db)
        company = СompanyDetailBaseModel.from_orm(company_db)
        response = make_response(
            jsonify(company.dict()),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @jwt_required()
    @is_user_company()
    @has_permission_obj_user_company()
    def delete(self):
        company_db = current_user.company
        db.session.delete(company_db)
        db.session.commit()
        return [],200
    @jwt_required()
    @is_user_company()
    def post(self):
        try:
            company = СompanyBaseModel.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(), 400
            )
            response.headers["Content-Type"] = "application/json"
            return response
        company_db = Сompany(**company.dict())
        db.session.add(company_db)
        db.session.commit()
        current_user.company = company_db
        db.session.commit()
        company = СompanyDetailBaseModel.from_orm(company_db)
        response = make_response(
            jsonify(company.dict()),
            201
        )
        response.headers["Content-Type"] = "application/json"
        return response
