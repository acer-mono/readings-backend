from models.Reading import Reading
from flask_restx import Resource
from schemas.UserSchema import users_schema
from flask_jwt_extended import jwt_required


class TableResource(Resource):
    @jwt_required()
    def get(self):
        #start_date = request.args.get('from')
        #end_date = request.args.get('to')
        #room_id = request.args.get('room')
        #format = request.args.get('format')
        readings = Reading.query.all()
        readings_json = users_schema.dump(readings)
        import wkhtmltopdf
        wkhtmltopdf.from_url('http://google.com', 'out.pdf')
        return []