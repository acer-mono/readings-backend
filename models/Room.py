from services.database import db


class Room(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '<Room %s>' % self.name
