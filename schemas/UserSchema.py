from services.config import ma
from models.User import User


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "login", "password", "isAdmin")
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
