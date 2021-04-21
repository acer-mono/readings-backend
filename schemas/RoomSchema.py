from services.config import ma
from models.Room import Room


class RoomSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = Room


room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
