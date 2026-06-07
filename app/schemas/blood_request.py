from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.donor import BloodGroup
from app.models.blood_request import RequestStatus


class BloodRequestCreate(BaseModel):
    patient_name: str
    blood_group: BloodGroup
    hospital_name: str
    required_date: date
    contact_number: str


class BloodRequestUpdate(BaseModel):
    patient_name: Optional[str] = None
    hospital_name: Optional[str] = None
    required_date: Optional[date] = None
    contact_number: Optional[str] = None


class StatusUpdate(BaseModel):
    status: RequestStatus


class BloodRequestOut(BaseModel):
    id: int
    patient_name: str
    blood_group: BloodGroup
    hospital_name: str
    required_date: date
    contact_number: str
    status: RequestStatus
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True