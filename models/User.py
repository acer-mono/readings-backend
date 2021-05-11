from services.database import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    readings = db.relationship('Reading', backref='owner_users')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def __repr__(self):
        return '<User: {}>'.format(self.id)
