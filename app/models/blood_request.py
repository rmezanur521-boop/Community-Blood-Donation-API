from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.session import Base
from app.models.donor import BloodGroup


class RequestStatus(str, enum.Enum):
    pending = "pending"
    fulfilled = "fulfilled"
    cancelled = "cancelled"


class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    blood_group = Column(Enum(BloodGroup), nullable=False)
    hospital_name = Column(String(200), nullable=False)
    required_date = Column(Date, nullable=False)
    contact_number = Column(String(20), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", back_populates="blood_requests")