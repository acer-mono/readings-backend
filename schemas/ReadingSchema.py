from services.config import ma
from models.Reading import Reading


class ReadingSchema(ma.Schema):
    class Meta:
        fields = ("id", "temperature", "humidity", "room_id", "user_id", "date")
        model = Reading


reading_schema = ReadingSchema()
readings_schema = ReadingSchema(many=True)
