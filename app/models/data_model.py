from app.connections.db import Base
from zoneinfo import ZoneInfo
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

def get_current_time():
    """Mengembalikan waktu saat ini dalam zona WIB"""
    utc_now = datetime.now(ZoneInfo("UTC"))
    return utc_now.astimezone(ZoneInfo("Asia/Jakarta"))

class Data(Base):
    __tablename__ = "data"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    juz_read = Column(Integer, nullable=False)
    last_juz = Column(Integer, nullable=False, default=0)
    total_khatam = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=get_current_time, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    users = relationship("Users", back_populates="data")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "juz_read": self.juz_read,
            "last_juz": self.last_juz,
            "total_khatam": self.total_khatam,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted,
            }
        }