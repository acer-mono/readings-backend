from services.config import ma
from models.Room import Room


class RoomSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Room

    id = ma.auto_field()
    name = ma.auto_field()
    readings = ma.auto_field()


room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
