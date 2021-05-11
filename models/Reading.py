from services.database import db
import datetime


class Reading(db.Model):
    __tablename__ = 'reading'
    __table_args__ = (
        db.UniqueConstraint('room_id', 'date'),
    )

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.DECIMAL(asdecimal=False), nullable=False)
    humidity = db.Column(db.DECIMAL(asdecimal=False), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DATE, default=datetime.date.today())

    def __repr__(self):
        return '<Reading: {}>'.format(self.id)
