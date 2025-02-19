import ast
import json
from flask_jwt_extended import get_jwt_identity
from app.services.progress_services import ProgressServices
from app.utils.auth.middleware import user_required

class ProgressControllers:
    @staticmethod
    @user_required()
    def get_progress_data():
        response = ProgressServices.progress_data()
        return response