from services.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Room %s>' % self.login
