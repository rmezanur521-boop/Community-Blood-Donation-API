from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.donor import BloodGroup
import math


class DonorCreate(BaseModel):
    blood_group: BloodGroup
    phone: str
    city: str
    address: Optional[str] = None
    last_donation_date: Optional[date] = None


class DonorUpdate(BaseModel):
    phone: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    last_donation_date: Optional[date] = None
    is_available: Optional[bool] = None


class DonorOut(BaseModel):
    id: int
    user_id: int
    blood_group: BloodGroup
    phone: str
    city: str
    address: Optional[str] = None
    last_donation_date: Optional[date] = None
    is_available: bool
    full_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class AvailabilityUpdate(BaseModel):
    is_available: bool


class PaginatedDonors(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    donors: list[DonorOut]

    @classmethod
    def build(
        cls,
        donors: list[DonorOut],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedDonors":
        return cls(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if page_size > 0 else 0,
            donors=donors,
        )