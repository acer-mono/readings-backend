from services.config import ma
from models.Reading import Reading


class ReadingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reading

    id = ma.auto_field()
    temperature = ma.auto_field()
    humidity = ma.auto_field()
    room_id = ma.auto_field()
    user_id = ma.auto_field()
    date = ma.auto_field()


reading_schema = ReadingSchema()
readings_schema = ReadingSchema(many=True)
