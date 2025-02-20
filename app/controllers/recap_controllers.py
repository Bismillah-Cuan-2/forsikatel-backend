import ast
import json
from flask_jwt_extended import get_jwt_identity
from app.services.recap_services import RecapServices
from app.utils.auth.middleware import user_required

class RecapControllers:
    @staticmethod
    @user_required()
    def get_recap_data():
        response = RecapServices.recap_data()
        return response