from services.config import ma
from models.User import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    login = ma.auto_field()
    password = ma.auto_field()
    isAdmin = ma.auto_field()
    roles = ma.auto_field()
    is_active = ma.auto_field()
    readings = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
