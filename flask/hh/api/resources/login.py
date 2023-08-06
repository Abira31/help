from flask_restful import Resource
from api import db
from api.models import User
from flask import jsonify,request,make_response
from werkzeug.security import check_password_hash
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_required
                                )

class LoginAPI(Resource):
    def post(self):
        email = request.json.get('email',None)
        password = request.json.get('password',None)
        user = db.session.query(User).filter(User.email==email).first()
        if user and check_password_hash(user.password,password):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            response = make_response(
                jsonify(access_token=access_token, refresh_token=refresh_token),
                200
            )
            response.headers["Content-Type"] = "application/json"
            return response
        return [],204

class RefreshLoginAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)