from models.User import User
from flask_restx import Resource
from schemas.UserSchema import users_schema
import flask_praetorian
from sqlalchemy import and_
from services.decorators import is_user_admin


class UserListResource(Resource):
    @flask_praetorian.auth_required
    @is_user_admin
    def get(self):
        user = flask_praetorian.current_user()
        user_id = user.id
        conds = [User.id != user_id]
        users = User.query.filter(and_(*conds))
        return users_schema.dump(users)
