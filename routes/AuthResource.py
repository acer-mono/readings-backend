from flask import request
from services.config import guard
from flask_restx import Resource


class LoginResource(Resource):
    def post(self):
        login = request.json['login']
        password = request.json['password']
        user = guard.authenticate(login, password)
        ret = {'access_token': guard.encode_jwt_token(user)}
        return ret, 200


class RefreshResource(Resource):
    def post(self):
        old_token = request.json['access_token']
        new_token = guard.refresh_jwt_token(old_token)
        ret = {'access_token': new_token}
        return ret, 200
