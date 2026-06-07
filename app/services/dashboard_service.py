from sqlalchemy.orm import Session
from app.repositories.donor_repository import DonorRepository
from app.repositories.blood_request_repository import BloodRequestRepository
from app.repositories.user_repository import UserRepository
from app.schemas.dashboard import DashboardStats


class DashboardService:
    def __init__(self, db: Session):
        self.donor_repo = DonorRepository(db)
        self.request_repo = BloodRequestRepository(db)
        self.user_repo = UserRepository(db)

    def get_stats(self) -> DashboardStats:
        return DashboardStats(
            total_donors=self.donor_repo.get_total_count(),
            available_donors=self.donor_repo.get_available_count(),
            active_requests=self.request_repo.get_active_count(),
            total_users=self.user_repo.get_total_count(),
            fulfilled_requests=self.request_repo.get_fulfilled_count(),
        )