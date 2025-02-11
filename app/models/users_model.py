from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app.constant.enums.regional import RegionalEnums

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name_husband = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    regional = Column(Enum(RegionalEnums), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def set_phone_number(self, var_phone_number):
        self.phone_number = generate_password_hash(var_phone_number)

    def check_phone_number(self, var_phone_number):
        return check_password_hash(self.phone_number, var_phone_number)
    
    data = relationship("Data", back_populates="users")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name_husband": self.name_husband,
            "phone_number": self.phone_number,
            "regional": self.regional,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
                }
        }