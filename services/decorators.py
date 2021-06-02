from functools import wraps
import flask_praetorian


def is_user_admin(f):
    @wraps(f)
    def check_is_user_admin(*args, **kwargs):
        user = flask_praetorian.current_user()
        if not user.isAdmin:
            return {"message": "Недостаточно прав"}, 403

        return f(*args, **kwargs)

    return check_is_user_admin

