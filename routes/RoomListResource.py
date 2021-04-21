from flask import request
from models.Room import Room, db
from flask_restful import Resource
from schemas.RoomSchema import rooms_schema, room_schema


class RoomListResource(Resource):
    def get(self):
        rooms = Room.query.all()
        return rooms_schema.dump(rooms)

    def post(self):
        new_room = Room(
            name=request.json['name']
        )
        db.session.add(new_room)
        db.session.commit()
        return room_schema.dump(new_room)