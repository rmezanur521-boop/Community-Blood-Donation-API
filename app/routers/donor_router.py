from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.schemas.donor import DonorCreate, DonorUpdate, DonorOut, PaginatedDonors, AvailabilityUpdate
from app.services.donor_service import DonorService
from app.dependencies.auth_dependency import get_current_user, require_donor
from app.models.user import User
from app.models.donor import BloodGroup

router = APIRouter(prefix="/donors", tags=["Donors"])


@router.post("/", response_model=DonorOut, status_code=status.HTTP_201_CREATED)
def create_donor_profile(
    data: DonorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_donor),
):
    return DonorService(db).create_profile(data, current_user)


@router.get("/", response_model=PaginatedDonors)
def list_donors(
    blood_group: Optional[BloodGroup] = Query(None),
    city: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DonorService(db).list_donors(blood_group, city, search, page, page_size)


@router.get("/{donor_id}", response_model=DonorOut)
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DonorService(db).get_donor(donor_id)


@router.put("/{donor_id}", response_model=DonorOut)
def update_donor(
    donor_id: int,
    data: DonorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DonorService(db).update_profile(donor_id, data, current_user)


@router.patch("/{donor_id}/availability", response_model=DonorOut)
def update_availability(
    donor_id: int,
    data: AvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DonorService(db).update_availability(donor_id, data, current_user)