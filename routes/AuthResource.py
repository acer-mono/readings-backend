from flask import request
from services.config import guard
from flask_restx import Resource
from models.User import User
from services.database import db


class LoginResource(Resource):
    def post(self):
        if len(db.session.query(User).all()) == 0:
            admin = User(login="admin", password="12345678", isAdmin=True, roles='admin')
            admin.hash_password()
            db.session.add(admin)
            db.session.commit()

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
