from services.config import ma, secret_key
from flask import Flask
from services.database import db
from services.config import api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db.init_app(app)
with app.app_context():
    db.create_all()

# config routes
ma.init_app(app)
api.init_app(app)

# jwt-token
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = secret_key

if __name__ == '__main__':
    app.run()
