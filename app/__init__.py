from flask import Flask, redirect, request
from app.config import DevelopmentConfig, ProductionConfig
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_cors import CORS

jwt = JWTManager()

load_dotenv()

def create_app(test_config=None, production_config=os.getenv("PRODUCTION_CONFIG")):
    app = Flask(__name__)
    
    if test_config is not None:
        app.config.from_object(test_config)
        
    if production_config is not None:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        
    jwt.init_app(app)
    
    CORS(app)
    
    @app.route("/")
    def index():
        return redirect("https://documenter.getpostman.com/view/31842216/2sAYBRGa1z")
    
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 204
    
    return app