from models.User import User
from flask_restx import Resource
from schemas.UserSchema import users_schema
import flask_praetorian
from sqlalchemy import and_


class UserListResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        user_id = flask_praetorian.current_user().id
        conds = [User.id != user_id]
        users = User.query.filter(and_(*conds))
        return users_schema.dump(users)
