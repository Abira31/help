from functools import wraps
from flask_jwt_extended import current_user
from flask import jsonify,make_response,request
from api import db
from api.models import User,Role
from sqlalchemy.orm import join
def is_admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if request.method == 'GET':
                return fn(*args, **kwargs)
            else:
                if current_user.is_admin:
                    return fn(*args, **kwargs)
                response = make_response(
                    jsonify(msg="Не достаточно прав"),403
                )
                response.headers["Content-Type"] = "application/json"
                return response
        return decorator
    return wrapper

def is_user_company():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if request.method == 'GET':
                    return fn(*args, **kwargs)
            role_db = db.session.query(Role).select_from(join(Role, User, User.roles))\
                .filter(Role.name == 'работодатель',User.id == current_user.id).first()
            if role_db is not None:
                return fn(*args, **kwargs)
            response = make_response(
                jsonify(msg="Не достаточно прав"), 403
            )
            response.headers["Content-Type"] = "application/json"
            return response
        return decorator
    return wrapper

def has_permission_obj_user_company():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.company is not None:
                    return fn(*args, **kwargs)
            response = make_response(
                jsonify(msg="Компания не найдена"), 204
            )
            response.headers["Content-Type"] = "application/json"
            return response
        return decorator
    return wrapper
