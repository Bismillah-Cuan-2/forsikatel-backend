from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.constant.enums.regional import RegionalEnums

class Users:
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    regional = Column(Enum(RegionalEnums), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "regional": self.regional,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
                }
        }