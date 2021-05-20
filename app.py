from services.config import ma, guard, secret_key
from flask import Flask
from flask_bcrypt import Bcrypt
from services.database import db
from services.exception_handlers import api
from models.User import User
from routes.RoomResource import RoomResource
from routes.AuthResource import RefreshResource
from routes.AuthResource import LoginResource
from routes.ReadingListResource import ReadingListResource
from routes.UserResource import UserResource
from routes.UserListResource import UserListResource
from routes.ReadingResource import ReadingResource
from routes.RoomListResource import RoomListResource
from routes.TableResource import TableResource
from routes.PlotResource import PlotResource
from flask_cors import CORS

app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db.init_app(app)
with app.app_context():
    db.create_all()

# config routes
ma.init_app(app)
api.init_app(app)

#cors
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# jwt-token
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = secret_key
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
guard.init_app(app, User)

api.add_resource(LoginResource, '/login')
api.add_resource(RefreshResource, '/refresh')
api.add_resource(ReadingResource, '/reading')
api.add_resource(ReadingListResource, '/readings')
api.add_resource(RoomResource, '/room')
api.add_resource(RoomListResource, '/rooms')
api.add_resource(UserResource, '/user')
api.add_resource(UserListResource, '/users')
api.add_resource(TableResource, '/table')
api.add_resource(PlotResource, '/plot')


if __name__ == '__main__':
    app.run()
