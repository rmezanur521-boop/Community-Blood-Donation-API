from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.database.session import Base


class BloodGroup(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    blood_group = Column(Enum(BloodGroup), nullable=False)
    phone = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    last_donation_date = Column(Date, nullable=True)
    is_available = Column(Boolean, default=True)

    user = relationship("User", back_populates="donor_profile")