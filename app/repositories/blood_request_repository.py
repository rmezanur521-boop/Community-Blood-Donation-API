from sqlalchemy.orm import Session
from app.models.blood_request import BloodRequest, RequestStatus
from typing import Optional


class BloodRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, request: BloodRequest) -> BloodRequest:
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def get_by_id(self, request_id: int) -> BloodRequest | None:
        return self.db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    def get_all(self, status: Optional[RequestStatus], skip: int, limit: int) -> list[BloodRequest]:
        query = self.db.query(BloodRequest)
        if status:
            query = query.filter(BloodRequest.status == status)
        return query.order_by(BloodRequest.created_at.desc()).offset(skip).limit(limit).all()

    def update(self, request: BloodRequest) -> BloodRequest:
        self.db.commit()
        self.db.refresh(request)
        return request

    def delete(self, request: BloodRequest) -> None:
        self.db.delete(request)
        self.db.commit()

    def get_active_count(self) -> int:
        return self.db.query(BloodRequest).filter(
            BloodRequest.status == RequestStatus.pending
        ).count()

    def get_fulfilled_count(self) -> int:
        return self.db.query(BloodRequest).filter(
            BloodRequest.status == RequestStatus.fulfilled
        ).count()