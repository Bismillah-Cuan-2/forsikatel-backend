from flask import jsonify
from sqlalchemy import func
from app.connections.db import Session
from app.utils.functions.normalizer import normalize_data
from app.models.users_model import Users
from app.constant.messages.user import UserMessages
from app.constant.messages.error import Error
from app.utils.validators.login_validator import LoginValidator
from app.utils.validators.register_validator import RegisterValidator

class UsersService:
    @staticmethod
    def create_user(data):
        with Session() as session:
            try:
                # Normalisasi name_husband untuk pencarian di query
                name_to_search = normalize_data(data["name_husband"])

                # Cek apakah name_husband yang telah dinormalisasi sudah ada di database
                check_name_husband = session.query(Users).filter(func.lower(func.replace(Users.name_husband, " ", "")) == name_to_search).first()
                
                if check_name_husband is not None:
                    return jsonify({"msg": UserMessages.NAME_ALREADY_EXIST}), 400
                
                new_user: Users = Users(
                    name_husband = data["name_husband"],
                    regional = data["regional"]
                )
                new_user.set_phone_number(data["phone_number"])
                
                session.add(new_user)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": UserMessages.SUCCESS_USER_REGISTER,
                "new_user_info": new_user.to_dict()
            }), 201
    
    @staticmethod
    def login_user(data):
        with Session() as session:
            try:
                # Normalisasi name_husband untuk pencarian di query
                name_to_search = normalize_data(data["name_husband"])

                # Cek apakah name_husband yang telah dinormalisasi sudah ada di database
                user_check = session.query(Users).filter(func.lower(func.replace(Users.name_husband, " ", "")) == name_to_search).first()
                
                if user_check is None:
                    return jsonify({"msg": UserMessages.NAME_NOT_EXIST}), 404
                
                if user_check.check_phone_number(data["phone_number"]):
                    payload = {
                        "user_id": user_check.id,
                        "name_husband": user_check.name_husband,
                        "regional": user_check.regional.value
                    }
                    
                    return {
                        "msg": UserMessages.LOGIN_SUCCESS,
                        "payload": payload
                    }
                
                else:
                    return jsonify({"msg": UserMessages.INCORRECT_PHONE_NUMBER}), 403
            except Exception as e:
                return jsonify(Error.messages(e)), 400
                
    @staticmethod
    def delete_user(data):
        with Session() as session:
            try:
                name_to_search = normalize_data(data["name_husband"])
                
                user_profile = session.query(Users).filter_by(func.lower(func.replace(Users.name_husband, " ", "")) == name_to_search, id=data["user_id"]).first()
                if not user_profile:
                    return jsonify({"msg": UserMessages.NAME_NOT_EXIST}), 404
                
                user_profile.is_deleted = True
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": UserMessages.SUCCESS_DELETE_USER
            }), 200
            