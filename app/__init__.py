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
        return redirect("https://www.postman.com/cuan33/workspace/cuan-2/collection/39870388-003398ac-ac89-4657-ac62-8c7bd46c219b?action=share&creator=39870388&active-environment=39870388-48f83279-5741-4408-8153-a3ccf31ffb59")
    
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 204
          
    from app.routes import hadist_kultum, seeds, users, setoran_ngaji, dashboard, progress

    app.register_blueprint(hadist_kultum, url_prefix="/api/v1/hadist-kultum")
    app.register_blueprint(seeds, url_prefix="/api/v1/seeds")
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(setoran_ngaji, url_prefix="/api/v1/setoran-ngaji")
    app.register_blueprint(dashboard, url_prefix="/api/v1/dashboard")
    app.register_blueprint(progress, url_prefix="/api/v1/progress")
    
    return app