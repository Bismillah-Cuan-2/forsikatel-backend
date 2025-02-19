from flask import json, request
from app.services.setoran_ngaji_services import Dataservices
from app.utils.auth.middleware import user_required
from flask_jwt_extended import get_jwt_identity
import ast
import json
class SetoranNgajiControllers:
    @staticmethod
    @user_required()
    def setoran_ngaji_controllers():
        payload = json.dumps(ast.literal_eval(get_jwt_identity()))
        payload = json.loads(payload)
        user_id = int(payload["user_id"])
        
        if request.method == "POST":
            data = request.json
            response = Dataservices.add_setoran(user_id, data["juz_read"])
        elif request.method == "GET":
            response = Dataservices.all_storage(user_id)
        return response
    
    @staticmethod
    @user_required()
    def progress_chart_controllers():
        payload = json.dumps(ast.literal_eval(get_jwt_identity()))
        payload = json.loads(payload)
        user_id = int(payload["user_id"])

        if request.method == "GET":
            response = Dataservices.get_progress_chart(user_id)
        return response