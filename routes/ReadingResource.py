from flask_restx import Resource
from models.Reading import Reading
from flask import request
from services.database import db
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from models.Room import Room
from models.User import User
from flask_jwt_extended import get_jwt_identity
from datetime import date
from schemas.ReadingSchema import reading_schema


class ReadingResource(Resource):
    @jwt_required()
    def post(self):
        temperature = request.json['temperature']
        humidity = request.json['humidity']

        user_id = get_jwt_identity()
        user = db.session.query(User).get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        room_id = request.json['room']
        room = db.session.query(Room).get(room_id)
        if not room:
            return {'message': 'Room not found'}, 404

        reading = Reading(owner_users=user, owner_rooms=room, temperature=temperature, humidity=humidity)
        db.session.add(reading)
        db.session.commit()
        return reading_schema.dump(reading), 200

    @jwt_required()
    def get(self):
        room_id = request.args.get('room')

        conds = [Reading.room_id == room_id, Reading.date == date.today()]
        reading_query = Reading.query.filter(or_(*conds))
        reading = reading_query.first()

        if not reading:
            return {'message': 'Reading not found'}, 404
        else:
            return reading_schema.dump(reading), 200

    @jwt_required()
    def put(self):
        temperature = request.json['temperature']
        humidity = request.json['humidity']
        room_id = request.json['room']

        conds = [Reading.room_id == room_id, Reading.date == date.today()]
        reading_query = Reading.query.filter(or_(*conds))
        reading = reading_query.first()

        if not reading:
            return {'message': 'Reading not found'}, 404
        else:
            reading.temperature = temperature
            reading.humidity = humidity
            db.session.add(reading)
            db.session.commit()
            return reading_schema.dump(reading), 200
