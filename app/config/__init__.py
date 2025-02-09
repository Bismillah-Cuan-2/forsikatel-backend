import os
from datetime import timedelta

class Config:
    SECRET_KEY  = os.getenv("SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
class ProductionConfig(Config):
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
class TestConfig():
    TESTING = True