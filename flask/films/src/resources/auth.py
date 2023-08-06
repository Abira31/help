from functools import wraps

from flask import request
from flask_restful import Resource
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
import jwt
import datetime

from src import db,app
from src.schemas.users import UserSchema
from src.models import User

class AuthRegister(Resource):
    user_schema = UserSchema()
    def post(self):
        try:
            user = self.user_schema.load(request.json,session=db.session)
        except ValidationError as e:
            return {"message":str(e)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message":"Such user exists"}, 409
        return self.user_schema.dump(user),201

class AuthLogin(Resource):
    def get(self):
        username = request.json.get('username',None)
        password = request.json.get('password',None)

        user = db.session.query(User).filter_by(username=username).first()
        if not user or  check_password_hash(user.password,username):
            return '',401
        token = jwt.encode(
            {
                "user_id":user.id,
                "exp":datetime.datetime.now() + datetime.timedelta(hours=1)
            },app.config['SECRET_KEY']
        )
        return jsonify({
            "token":token
        })


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')
        if not token:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = db.session.query(User).filter_by(uuid=uuid).first()
        if not user:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper