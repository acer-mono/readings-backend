from routes.RoomListResource import RoomListResource
from routes.RoomResource import RoomResource
from routes.UserResource import UserResource
from services.config import ma
from flask import Flask
from flask_restful import Api
from services.database import db

app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db.init_app(app)
with app.app_context():
    db.create_all()

# config routes
ma.init_app(app)
api = Api(app)

# routes
api.add_resource(RoomListResource, '/rooms')
api.add_resource(RoomResource, '/room/<int:room_id>')
api.add_resource(UserResource, '/user')

if __name__ == '__main__':
    app.run()
