from flask import request
from models.Room import Room
from flask_restx import Resource
from schemas.RoomSchema import room_schema
import flask_praetorian
from services.database import db


class RoomResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        room_id = request.args.get('id')
        room = Room.query.get_or_404(room_id)
        return room_schema.dump(room)

    @flask_praetorian.auth_required
    def post(self):
        new_room = Room(
            name=request.json['name']
        )

        db.session.add(new_room)
        db.session.commit()
        return room_schema.dump(new_room)

    @flask_praetorian.auth_required
    def put(self):
        room_id = request.json['id']
        name = request.json['name']

        room = Room.query.get_or_404(room_id)
        room.name = name

        db.session.add(room)
        db.session.commit()
        return room_schema.dump(room)

    @flask_praetorian.auth_required
    def delete(self):
        room_id = request.json['id']

        room = Room.query.get_or_404(room_id)

        db.session.delete(room)
        db.session.commit()
        return room_schema.dump(room)
