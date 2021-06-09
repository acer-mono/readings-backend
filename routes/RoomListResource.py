from models.Room import Room
from flask_restx import Resource
from schemas.RoomSchema import rooms_schema
import flask_praetorian


class RoomListResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        rooms = Room.query.all()
        return rooms_schema.dump(rooms)
