from flask import Blueprint
from app.controllers.hadist_kultum_controllers import HadistKultumControllers

hadist_kultum = Blueprint("hadist-kultum", __name__)
hadist_kultum.add_url_rule("/hadist-kultum", view_func=HadistKultumControllers.get_daily_hadist, methods=["GET"])