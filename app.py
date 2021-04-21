from routes.RoomListResource import RoomListResource
from routes.RoomResource import RoomResource
from routes.UserResource import UserResource
from routes.LoginResource import LoginResource
from services.config import ma, secret_key
from flask import Flask
from flask_restful import Api
from services.database import db
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
api = Api(app)

# jwt-token
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = secret_key

# routes
api.add_resource(RoomListResource, '/rooms')
api.add_resource(RoomResource, '/room/<int:room_id>')
api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run()
