from models.User import User
from flask_restx import Resource
from schemas.UserSchema import users_schema
import flask_praetorian


class UserListResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
