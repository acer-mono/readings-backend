from models.Room import Room
from flask_restx import Resource
from schemas.RoomSchema import room_schema
from flask_jwt_extended import jwt_required


class RoomResource(Resource):
    @jwt_required()
    def get(self, room_id):
        room = Room.query.get_or_404(room_id)
        return room_schema.dump(room)