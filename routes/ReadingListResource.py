from flask import request
from models.Reading import Reading
from flask_restx import Resource
from schemas.ReadingSchema import readings_schema
import flask_praetorian


class ReadingListResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        start_date = request.args.get('from')
        end_date = request.args.get('to')
        room_id = request.args.get('room')

        readings = Reading.query.filter(Reading.date.between(start_date, end_date), Reading.room_id == room_id)
        return readings_schema.dump(readings)
