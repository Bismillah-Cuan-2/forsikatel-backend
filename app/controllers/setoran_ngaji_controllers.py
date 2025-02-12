from flask import jsonify, request
from app.services.setoran_ngaji_services import Dataservices

class SetoranNgajiControllers:
    @staticmethod
    def setoran_ngaji_controllers(payload):
        if request.method == "POST":
            data = request.json
            response = Dataservices.add_setoran(payload, data)
        elif request.method == "GET":
            response = Dataservices.all_storage(payload)
        return response