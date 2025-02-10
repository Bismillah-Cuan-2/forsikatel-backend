from flask import jsonify, request
from app.services.hadist_kultum_services import HadistKultumServices

class HadistKultumControllers:
    @staticmethod
    def get_daily_hadist():
        if request.method == 'GET':
            response = HadistKultumServices.get_daily_hadist()
        return response