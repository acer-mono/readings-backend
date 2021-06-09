import flask_praetorian
from flask_restx import Resource
from models.User import User
from flask import request
from services.database import db
from schemas.UserSchema import user_schema
from services.decorators import is_user_admin


class UserResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        user = flask_praetorian.current_user()
        return user_schema.dump(user)

    @flask_praetorian.auth_required
    @is_user_admin
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
    @is_user_admin
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
    @is_user_admin
    def delete(self):
        user_id = request.json['id']

        user = User.query.get_or_404(user_id)

        if user and len(user.readings) > 0:
            return {"message": "Невозможно удалить пользователя"}, 400

        db.session.delete(user)
        db.session.commit()
        return user_schema.dump(user)
