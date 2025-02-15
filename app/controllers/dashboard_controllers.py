import ast
import json
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.services.dashboard_services import DashboardServices
from app.utils.auth.middleware import user_required 

class DashboardControllers:
    @staticmethod
    @user_required()
    def get_dashboard_data():
        payload = json.dumps(ast.literal_eval(get_jwt_identity()))
        payload = json.loads(payload)
        response = DashboardServices.dashboard_data(payload)
        return response