from app.connections.db import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, Enum, String
from datetime import datetime, timezone

class HadistKultum(Base):
    __tablename__ = "hadist_kultum"
    id = Column(Integer, primary_key=True, nullable=False)
    hadist = Column(String(100000), nullable=False)
    kultum = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    day = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "hadist": self.hadist,
            "kultum": self.kultum,
            "day": self.day,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }