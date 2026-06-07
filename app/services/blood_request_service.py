from sqlalchemy.orm import Session
from app.repositories.blood_request_repository import BloodRequestRepository
from app.schemas.blood_request import BloodRequestCreate, BloodRequestUpdate, StatusUpdate
from app.models.blood_request import BloodRequest, RequestStatus
from app.models.user import User, UserRole
from app.core.exceptions import NotFoundException, ForbiddenException
from typing import Optional


class BloodRequestService:
    def __init__(self, db: Session):
        self.repo = BloodRequestRepository(db)

    def create_request(self, data: BloodRequestCreate, current_user: User) -> BloodRequest:
        request = BloodRequest(
            patient_name=data.patient_name,
            blood_group=data.blood_group,
            hospital_name=data.hospital_name,
            required_date=data.required_date,
            contact_number=data.contact_number,
            created_by=current_user.id,
        )
        return self.repo.create(request)

    def get_request(self, request_id: int) -> BloodRequest:
        request = self.repo.get_by_id(request_id)
        if not request:
            raise NotFoundException("Blood request not found")
        return request

    def list_requests(self, status: Optional[RequestStatus], page: int, page_size: int) -> list[BloodRequest]:
        skip = (page - 1) * page_size
        return self.repo.get_all(status, skip, page_size)

    def update_status(self, request_id: int, data: StatusUpdate, current_user: User) -> BloodRequest:
        request = self.repo.get_by_id(request_id)
        if not request:
            raise NotFoundException("Blood request not found")
        if request.created_by != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenException("Access denied")

        request.status = data.status
        return self.repo.update(request)

    def delete_request(self, request_id: int, current_user: User) -> dict:
        request = self.repo.get_by_id(request_id)
        if not request:
            raise NotFoundException("Blood request not found")
        if request.created_by != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenException("Access denied")

        self.repo.delete(request)
        return {"message": "Blood request deleted successfully"}