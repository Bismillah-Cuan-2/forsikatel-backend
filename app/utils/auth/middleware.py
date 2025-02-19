from flask import jsonify
import json
from functools import wraps
from app.constant.messages.user import  UserMessages
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users_model import Users
from app.connections.db import Session

# Custom decorator to check division
def user_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_view(*args, **kwargs):
            payload = eval(get_jwt_identity())
            with Session() as session:
                user = session.query(Users).filter_by(name_husband = payload["name_husband"])
                if user is None:
                    return jsonify({"msg": UserMessages.NAME_NOT_EXIST}), 404
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper