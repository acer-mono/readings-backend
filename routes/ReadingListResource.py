from models.Reading import Reading
from flask_restx import Resource
from schemas.ReadingSchema import readings_schema
from flask_jwt_extended import jwt_required


class ReadingListResource(Resource):
    @jwt_required()
    def get(self):
        readings = Reading.query.all()
        return readings_schema.dump(readings)
