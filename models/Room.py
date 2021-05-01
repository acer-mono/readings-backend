from services.database import db


class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    readings = db.relationship('Reading', backref='owner_rooms')

    def __repr__(self):
        return '<Room: {}>'.format(self.id)
