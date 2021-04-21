from flask_restx import Resource
from models.Reading import Reading
from flask import request
from services.database import db
from flask_jwt_extended import jwt_required


class ReadingResource(Resource):
    @jwt_required()
    def post(self):
        temperature = request.json['temperature']
        humidity = request.json['humidity']
        # здесь должно быть получение юзера на основе текущего токена
        user = request.json['user']
        # здесь должно быть получение комнаты на основе текущего значения
        room = request.json['room']
        reading = Reading(user=user, room=room, temperature=temperature, humidity=humidity)
        db.session.add(reading)
        db.session.commit()
        return {'id': str(reading.id)}, 200
