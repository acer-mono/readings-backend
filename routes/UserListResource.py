from models.User import User
from flask_restx import Resource
from schemas.UserSchema import users_schema
from flask_jwt_extended import jwt_required


class UserListResource(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
