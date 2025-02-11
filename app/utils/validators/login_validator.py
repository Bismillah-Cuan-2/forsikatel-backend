from pydantic import BaseModel, FieldValidationInfo, field_validator
import re

class LoginValidator(BaseModel):
    name_husband: str
    phone_number: str
    
    @field_validator('name_husband')
    def validate_name_husband(cls, name_husband: str, info: FieldValidationInfo):
        if "-" not in name_husband:
            raise ValueError('Name must contain a hyphen (-) separating the names.')
        return name_husband
    
    @field_validator('phone_number')
    def validate_phone_number(cls, phone_number: str, info: FieldValidationInfo):
        if len(phone_number) not in (10, 11, 12, 13):
            raise ValueError("Phone number must be 10 until 13 digits long.")
        if not re.search(r'\d+$', phone_number):
            raise ValueError('Phone number must contain only numbers.')
        return phone_number