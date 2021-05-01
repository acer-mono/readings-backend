from flask import request
from flask_jwt_extended import create_access_token
from models.User import User
from flask_restx import Resource
import datetime


class LoginResource(Resource):
    def post(self):
        user = User.query.filter_by(login=request.json['login']).first()
        authorized = user.check_password(request.json['password'])
        if not authorized:
            return {'message': 'Login or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
