import flask_praetorian
from flask_restx import Resource
from models.User import User
from flask import request
from services.database import db
from schemas.UserSchema import user_schema


class UserResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        user_id = request.args.get('id')

        user = User.query.get_or_404(user_id)

        return user_schema.dump(user)

    @flask_praetorian.auth_required
    def post(self):
        login = request.json['login']
        password = request.json['password']
        is_admin = request.json['is_admin']
        if not is_admin:
            role = 'user'
        else:
            role = 'admin'

        user = User(login=login, password=password, isAdmin=bool(is_admin), roles=role)
        user.hash_password()

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)

    @flask_praetorian.auth_required
    def put(self):
        user_id = request.json['id']
        login = request.json['login']
        password = request.json['password']
        is_admin = request.json['is_admin']

        user = User.query.get_or_404(user_id)
        user.login = login
        user.password = password
        user.isAdmin = bool(is_admin)
        user.hash_password()

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)

    @flask_praetorian.auth_required
    def delete(self):
        user_id = request.json['id']

        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()
        return user_schema.dump(user)
