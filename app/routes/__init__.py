from flask import Blueprint
from app.controllers.hadist_kultum_controllers import HadistKultumControllers
from app.controllers.user_controllers import UsersController
from app.controllers.seeds_controllers import seeds_controller

seeds = Blueprint("seeds", __name__)
seeds.add_url_rule("/", view_func=seeds_controller, methods=["GET", "POST", "DELETE"])

users = Blueprint("users", __name__)
users.add_url_rule("/register", view_func=UsersController.register_user, methods=["POST"])
users.add_url_rule("/login", view_func=UsersController.login_user, methods=["POST"])
users.add_url_rule("/delete", view_func=UsersController.delete_user, methods=["DELETE"])

hadist_kultum = Blueprint("hadist_kultum", __name__)
hadist_kultum.add_url_rule("/", view_func=HadistKultumControllers.get_daily_hadist, methods=["GET", "POST"])
