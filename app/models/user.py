from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.session import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    donor = "donor"
    requester = "requester"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.requester, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    donor_profile = relationship("Donor", back_populates="user", uselist=False)
    blood_requests = relationship("BloodRequest", back_populates="creator")