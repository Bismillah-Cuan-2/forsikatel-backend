from flask import request
from app.services.seeds_services import SeedsService

def seeds_controller():
    data = request.json
    
    if request.method == "GET":
        response = SeedsService.show_seeds(data)
        
        return response
    
    if request.method == "POST":
        response = SeedsService.generate_all_seed(data)
        
        return response
    
    if request.method == "DELETE":
        response = SeedsService.clear_seeds(data)
        
        return response