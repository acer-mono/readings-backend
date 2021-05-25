from models.Room import Room
from flask_restx import Resource
from schemas.RoomSchema import rooms_schema
import flask_praetorian


class RoomListResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        user = flask_praetorian.current_user()
        if not user.isAdmin:
            return {"message": "Недостаточно прав"}, 403
        rooms = Room.query.all()
        return rooms_schema.dump(rooms)
