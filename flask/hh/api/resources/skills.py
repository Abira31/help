from flask_restful import Resource
from api.models import Skills
from api import db
from flask import jsonify,request,make_response
from api.schemas.skills import SkillsBase,SkillsDetailBase
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
from api.core.permission import is_admin
class SkillsAPI(Resource):
    @jwt_required()
    @is_admin()
    def get(self,id=None):
        if not id:
            skills_db = db.session.query(Skills).all()
            skills = [SkillsBase.from_orm(s) for s in skills_db]
            response = make_response(
                jsonify([s.dict() for s in skills]),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        skills_db = db.session.query(Skills).filter_by(id=id).first()
        if not skills_db:
            return [],204
        skills_db = SkillsDetailBase.from_orm(skills_db)
        response = make_response(
            jsonify(skills_db.dict()),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    @jwt_required()
    @is_admin()
    def post(self):
        try:
            skills = SkillsDetailBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                jsonify(e.json()),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        skills_db = Skills(**skills.dict())
        db.session.add(skills_db)
        db.session.commit()
        skills = SkillsBase.from_orm(skills_db)
        response = make_response(
            jsonify(skills.dict()),
            201,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    @jwt_required()
    @is_admin()
    def put(self,id):
        skills_db = db.session.query(Skills).filter_by(id=id).first()
        if not skills_db:
            return [],204
        try:
            skills = SkillsDetailBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                jsonify(e.json()),
                400
            )
            response.headers["Content-Type"] = "application/json"
            return response
        skills_db.name = skills.name
        db.session.add(skills_db)
        db.session.commit()
        skills = SkillsBase.from_orm(skills_db)
        response = make_response(
            jsonify(skills.dict()),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    @jwt_required()
    @is_admin()
    def delete(self,id):
        skills_db = db.session.query(Skills).filter_by(id=id).first()
        if not skills_db:
            return [],204
        db.session.delete(skills_db)
        db.session.commit()
        return [],200



