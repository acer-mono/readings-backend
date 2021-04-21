from flask import request
from models.Room import Room, db
from flask_restx import Resource
from schemas.RoomSchema import rooms_schema, room_schema
from flask_jwt_extended import jwt_required


class RoomListResource(Resource):
    @jwt_required()
    def get(self):
        rooms = Room.query.all()
        return rooms_schema.dump(rooms)

    @jwt_required()
    def post(self):
        new_room = Room(
            name=request.json['name']
        )
        db.session.add(new_room)
        db.session.commit()
        return room_schema.dump(new_room)