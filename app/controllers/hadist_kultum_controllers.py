from flask import jsonify, request
from app.services.hadist_kultum_services import HadistKultumServices

class HadistKultumControllers:
    @staticmethod
    def get_daily_hadist(payload):
        _ = payload
        if request.method == "GET":
            response = HadistKultumServices.get_daily_hadist()
        return response

    def load_hadist_kultum_from_excel():
        if request.method == "POST":
            data = request.json
            response = HadistKultumServices.load_hadist_kultum_from_excel(data)
        return response