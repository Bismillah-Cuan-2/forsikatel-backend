from flask import request, jsonify
from app.utils.validators.login_validator import LoginValidator
from app.utils.validators.register_validator import RegisterValidator
from pydantic import ValidationError
from app.services.user_services import UsersService
from app.constant.messages.error import Error
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

class UsersController:
    
    @staticmethod
    def register_user():
        data = request.json
        try:
            register_validator = RegisterValidator.model_validate(data)
        except ValidationError as e:
            return jsonify(Error.messages(e)), 400
            
        response = UsersService.create_user(register_validator.model_dump())
        
        return response
    
    @staticmethod
    def login_user():
        data = request.json
        try:
            login_validator = LoginValidator.model_validate(data)
        except ValidationError as e:
            return jsonify(Error.messages(e)), 400
            
        response = UsersService.login_user(login_validator.model_dump())
        
        if "payload" in response:
            payload = response["payload"]
            print(payload)
            access_token = create_access_token(identity=f"{payload}")
            refresh_token = create_refresh_token(identity=f"{payload}")
            
            return jsonify({
                "msg": response["msg"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return response
    
    @staticmethod
    def delete_user(payload):
        _ = payload
        data = request.json
        response =UsersService.delete_user(data)
        
        return response
    