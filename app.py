from services.config import ma, secret_key
from flask import Flask
from services.database import db
from services.exception_handlers import api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from routes.RoomResource import RoomResource
from routes.AuthResource import AuthResource
from routes.ReadingListResource import ReadingListResource
from routes.UserResource import UserResource
from routes.UserListResource import UserListResource
from routes.ReadingResource import ReadingResource
from routes.RoomListResource import RoomListResource

app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db.init_app(app)
with app.app_context():
    db.create_all()

# config routes
ma.init_app(app)
api.init_app(app)

api.add_resource(AuthResource, '/auth')
api.add_resource(ReadingResource, '/reading')
api.add_resource(ReadingListResource, '/readings')
api.add_resource(RoomResource, '/room')
api.add_resource(RoomListResource, '/rooms')
api.add_resource(UserResource, '/user')
api.add_resource(UserListResource, '/users')

# jwt-token
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = secret_key

if __name__ == '__main__':
    app.run()
