from flask_restx import Api
import sqlalchemy
import flask_buzz

api = Api()
flask_buzz.FlaskBuzz.register_error_handler_with_flask_restplus(api)


@api.errorhandler(sqlalchemy.exc.OperationalError)
def handle_operational_error(e):
    return {'message': 'Невозможно совершить операцию. Обратитесь к администратору.'}, 500


@api.errorhandler(sqlalchemy.exc.IntegrityError)
def handle_integrity_error(e):
    return {'message': 'Невозможно совершить операцию. Проверьте данные.'}, 400


@api.errorhandler(Exception)
def catch_all_handler(e):
    return {'message': 'Уупс... Что-то пошло не так:('}, 500