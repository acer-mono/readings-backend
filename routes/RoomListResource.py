from models.Room import Room
from flask_restx import Resource
from schemas.RoomSchema import rooms_schema
from flask_jwt_extended import jwt_required


class RoomListResource(Resource):
    @jwt_required()
    def get(self):
        rooms = Room.query.all()
        return rooms_schema.dump(rooms)

