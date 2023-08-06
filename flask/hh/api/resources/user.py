from flask_restful import Resource
from api.models import User,Role,Resume
from flask import jsonify,request,make_response
from api.schemas.user import UserBase,UserDetailBase
from api.schemas.resumes import ResumesBase,ResumesSaveBase
from pydantic import ValidationError
from api import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import join
from flask_jwt_extended import current_user,jwt_required

class UserAPI(Resource):
    @jwt_required()
    def get(self):
        user = UserDetailBase.from_orm(current_user)
        response = make_response(
            jsonify(user.dict(exclude={"is_admin","is_active","password"})),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    def post(self):
        try:
            user = UserBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(),400
            )
            response.headers["Content-Type"] = "application/json"
            return response

        user_db = User(**user.dict())
        try:
            db.session.add(user_db)
            db.session.commit()
            return [],201
        except IntegrityError:
            db.session.rollback()
            response = make_response(
                {"msg":"Пользователь с такой почтой уже существует"}, 400
            )
            response.headers["Content-Type"] = "application/json"
            return response

class UserRoleAPI(Resource):
    @jwt_required()
    def post(self):
        roles = request.json.get('roles', None)
        roles_db = db.session.query(Role).filter(Role.id.in_(roles)).all()
        if len(roles_db) > 0:
            current_user.roles.clear()
            for role in roles_db:
                current_user.roles.append(role)
            db.session.commit()
            response = make_response(
                {"msg": "Роль(и) добавлена(ы)"}, 201
            )
            response.headers["Content-Type"] = "application/json"
            return response
        response = make_response(
            {"msg": "Роль(и) с таким(и) индентификатором(рами) отсутсвуют"}, 204
        )
        response.headers["Content-Type"] = "application/json"
        return response

class UserResumesAPI(Resource):
    @jwt_required()
    def get(self,id=None):
        if not id:
            resumes = [ResumesBase.from_orm(resume) for resume in current_user.resumes]

            response = make_response(
                jsonify([resume.dict() for resume in resumes]),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        resume_db = db.session.query(Resume).select_from(join(Resume,User,User.resumes)).filter(Resume.id==id,User.id==current_user.id).first()
        if resume_db is not None:
            resume = ResumesBase.from_orm(resume_db)
            response = make_response(
                jsonify(resume.dict(exclude={"id"})),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        return [],204

    @jwt_required()
    def post(self):
        try:
            resume = ResumesSaveBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(), 400,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        resume_db = Resume(**resume.dict())
        db.session.add(resume_db)
        db.session.commit()
        current_user.resumes.append(resume_db)
        db.session.commit()
        resume = ResumesBase.from_orm(resume_db)
        response = make_response(
            jsonify(resume.dict()),
            201,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @jwt_required()
    def put(self,id):
        try:
            resume = ResumesSaveBase.parse_obj(request.json)
        except ValidationError as e:
            response = make_response(
                e.json(), 400,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        resume_db = db.session.query(Resume).select_from(join(Resume, User, User.resumes)).filter(Resume.id == id,
                                                                                                  User.id == current_user.id).first()
        if resume_db is not None:
            for key,value in resume.dict().items():
                setattr(resume_db,key,value)
            db.session.commit()
            db.session.refresh(resume_db)
            resume = ResumesSaveBase.from_orm(resume_db)
            response = make_response(
                jsonify(resume.dict()),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        return [], 204

    @jwt_required()
    def delete(self,id):
        resume_db = db.session.query(Resume).select_from(join(Resume, User, User.resumes)).filter(Resume.id == id,
                                                                                                  User.id == current_user.id).first()
        if resume_db is not None:
            db.session.delete(resume_db)
            db.session.commit()
            return [],200
        return [],204



