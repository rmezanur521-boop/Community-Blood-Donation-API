from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.schemas.blood_request import BloodRequestCreate, BloodRequestOut, StatusUpdate
from app.services.blood_request_service import BloodRequestService
from app.dependencies.auth_dependency import get_current_user, require_requester
from app.models.user import User
from app.models.blood_request import RequestStatus

router = APIRouter(prefix="/requests", tags=["Blood Requests"])


@router.post("/", response_model=BloodRequestOut, status_code=status.HTTP_201_CREATED)
def create_request(
    data: BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_requester),
):
    return BloodRequestService(db).create_request(data, current_user)


@router.get("/", response_model=list[BloodRequestOut])
def list_requests(
    status: Optional[RequestStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BloodRequestService(db).list_requests(status, page, page_size)


@router.get("/{request_id}", response_model=BloodRequestOut)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BloodRequestService(db).get_request(request_id)


@router.patch("/{request_id}/status", response_model=BloodRequestOut)
def update_status(
    request_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BloodRequestService(db).update_status(request_id, data, current_user)


@router.delete("/{request_id}", status_code=status.HTTP_200_OK)
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BloodRequestService(db).delete_request(request_id, current_user)