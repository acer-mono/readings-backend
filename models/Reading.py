from sqlalchemy.orm import backref

from services.database import db
import datetime


class Reading(db.Model):
    __tablename__ = 'reading'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.DECIMAL(asdecimal=False), nullable=False)
    humidity = db.Column(db.DECIMAL(asdecimal=False), nullable=False)
    room = db.Column(db.Integer, db.ForeignKey('room.id'), unique=True, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    datetime = db.Column(db.DATETIME, default=datetime.datetime.utcnow)
