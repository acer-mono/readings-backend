from flask_restx import Resource
from models.Reading import Reading
from flask import request
from services.database import db
import flask_praetorian
from sqlalchemy import and_
from models.Room import Room
from datetime import date
from schemas.ReadingSchema import reading_schema


class ReadingResource(Resource):
    @flask_praetorian.auth_required
    def post(self):
        temperature = request.json['temperature']
        humidity = request.json['humidity']

        user = flask_praetorian.current_user()
        if not user:
            return {'message': 'Current user is not found'}, 400

        room_id = request.json['room']
        room = db.session.query(Room).get(room_id)
        if not room:
            return {'message': 'Room not found'}, 404

        reading = Reading(owner_users=user, owner_rooms=room, temperature=temperature, humidity=humidity)
        db.session.add(reading)
        db.session.commit()
        return reading_schema.dump(reading), 200

    @flask_praetorian.auth_required
    def get(self):
        room_id = request.args.get('room')

        conds = [Reading.room_id == room_id, Reading.date == date.today()]
        reading_query = Reading.query.filter(and_(*conds))
        reading = reading_query.first()

        if not reading:
            return {'message': 'Reading not found'}, 404
        else:
            return reading_schema.dump(reading), 200

    @flask_praetorian.auth_required
    def put(self):
        temperature = request.json['temperature']
        humidity = request.json['humidity']
        room_id = request.json['room']

        conds = [Reading.room_id == room_id, Reading.date == date.today()]
        reading_query = Reading.query.filter(and_(*conds))
        reading = reading_query.first()

        if not reading:
            return {'message': 'Reading not found'}, 404
        else:
            reading.temperature = temperature
            reading.humidity = humidity
            db.session.add(reading)
            db.session.commit()
            return reading_schema.dump(reading), 200
