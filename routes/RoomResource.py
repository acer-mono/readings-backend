from models.Room import Room
from flask_restful import Resource
from schemas.RoomSchema import room_schema


class RoomResource(Resource):
    def get(self, room_id):
        room = Room.query.get_or_404(room_id)
        return room_schema.dump(room)