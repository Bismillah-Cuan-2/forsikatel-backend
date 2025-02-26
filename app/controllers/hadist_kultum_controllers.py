from flask import jsonify, request
from app.services.hadist_kultum_services import HadistKultumServices
from app.utils.auth.middleware import user_required
from app.constant.messages.auth import AuthMessages

class HadistKultumControllers:
    @staticmethod
    @user_required()
    def get_daily_hadist():
        if request.method == "GET":
            response = HadistKultumServices.get_daily_hadist()
        return response
    
    @staticmethod
    def load_hadist_kultum_from_excel():
        if request.method == "POST":
            data = request.json
            response = HadistKultumServices.load_hadist_kultum_from_excel(data)
        return response