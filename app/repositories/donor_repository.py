from sqlalchemy.orm import Session, joinedload
from app.models.donor import Donor, BloodGroup
from app.models.user import User
from typing import Optional


class DonorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donor: Donor) -> Donor:
        self.db.add(donor)
        self.db.commit()
        self.db.refresh(donor)
        return donor

    def get_by_id(self, donor_id: int) -> Donor | None:
        return (
            self.db.query(Donor)
            .options(joinedload(Donor.user))
            .filter(Donor.id == donor_id)
            .first()
        )

    def get_by_user_id(self, user_id: int) -> Donor | None:
        return self.db.query(Donor).filter(Donor.user_id == user_id).first()

    def get_all(
        self,
        blood_group: Optional[BloodGroup],
        city: Optional[str],
        search: Optional[str],
        skip: int,
        limit: int,
    ) -> tuple[list[Donor], int]:
        query = self.db.query(Donor).options(joinedload(Donor.user))

        if blood_group:
            query = query.filter(Donor.blood_group == blood_group)
        if city:
            query = query.filter(Donor.city.ilike(f"%{city}%"))
        if search:
            query = query.join(Donor.user).filter(
                User.full_name.ilike(f"%{search}%")
            )

        total = query.count()
        donors = query.offset(skip).limit(limit).all()
        return donors, total

    def update(self, donor: Donor) -> Donor:
        self.db.commit()
        self.db.refresh(donor)
        return donor

    def get_available_count(self) -> int:
        return self.db.query(Donor).filter(Donor.is_available == True).count()

    def get_total_count(self) -> int:
        return self.db.query(Donor).count()