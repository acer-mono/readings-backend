from models.User import User
from flask_restx import Resource
from schemas.UserSchema import users_schema
import flask_praetorian
from sqlalchemy import and_


class UserListResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        user = flask_praetorian.current_user()
        if not user.isAdmin:
            return {"message": "Недостаточно прав"}, 403
        user_id = user.id
        conds = [User.id != user_id]
        users = User.query.filter(and_(*conds))
        return users_schema.dump(users)
