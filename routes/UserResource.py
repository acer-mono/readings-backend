from flask_restx import Resource
from models.User import User
from flask import request
from services.database import db


class UserResource(Resource):
    def post(self):
        login = request.json['login']
        password = request.json['password']
        user = User(login=login, password=password)
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return {'id': str(user.id)}, 200
