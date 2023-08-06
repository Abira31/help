from flask_restful import Resource
from api.models import Role
from api import db
from flask import jsonify,request,make_response
from api.schemas.role import RolesBase,RoleDetailBase
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
from api.core.permission import is_admin
class RoleAPI(Resource):
    def get(self,id=None):
        if not id:
            roles_db = db.session.query(Role).all()
            roles = [RolesBase.from_orm(role) for role in roles_db]
            response = make_response(
                jsonify([role.dict() for role in roles]),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        role_db = db.session.query(Role).filter_by(id=id).first()
        if not role_db:
            return [],204
        roles = RoleDetailBase.from_orm(role_db)
        response = make_response(
            jsonify(roles.dict()),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @jwt_required()
    @is_admin()
    def post(self):
        try:
            role = RoleDetailBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(),400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        role_db = Role(**role.dict())
        db.session.add(role_db)
        db.session.commit()
        role = RolesBase.from_orm(role_db)
        response = make_response(
            jsonify(role.dict()),
            201,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @jwt_required()
    @is_admin()
    def put(self,id):
        role_db = db.session.query(Role).filter_by(id=id).first()
        if not role_db:
            return [],204
        try:
            role = RoleDetailBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(),400,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        role_db.name = role.name
        db.session.add(role_db)
        db.session.commit()
        role = RolesBase.from_orm(role_db)
        response = make_response(
            jsonify(role.dict()),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @jwt_required()
    @is_admin()
    def delete(self,id):
        role_db = db.session.query(Role).filter_by(id=id).first()
        if not role_db:
            return [],204
        db.session.delete(role_db)
        db.session.commit()
        return [],200



