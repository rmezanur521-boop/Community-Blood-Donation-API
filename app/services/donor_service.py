from sqlalchemy.orm import Session
from app.repositories.donor_repository import DonorRepository
from app.schemas.donor import (
    DonorCreate, DonorUpdate, DonorOut,
    PaginatedDonors, AvailabilityUpdate
)
from app.models.donor import Donor, BloodGroup
from app.models.user import User, UserRole
from app.core.exceptions import ConflictException, NotFoundException, ForbiddenException
from typing import Optional


class DonorService:
    def __init__(self, db: Session):
        self.repo = DonorRepository(db)

    def create_profile(self, data: DonorCreate, current_user: User) -> Donor:
        existing = self.repo.get_by_user_id(current_user.id)
        if existing:
            raise ConflictException("Donor profile already exists for this user")

        donor = Donor(
            user_id=current_user.id,
            blood_group=data.blood_group,
            phone=data.phone,
            city=data.city,
            address=data.address,
            last_donation_date=data.last_donation_date,
        )
        return self.repo.create(donor)

    def get_donor(self, donor_id: int) -> DonorOut:
        donor = self.repo.get_by_id(donor_id)
        if not donor:
            raise NotFoundException("Donor not found")

        return DonorOut(
            id=donor.id,
            user_id=donor.user_id,
            blood_group=donor.blood_group,
            phone=donor.phone,
            city=donor.city,
            address=donor.address,
            last_donation_date=donor.last_donation_date,
            is_available=donor.is_available,
            full_name=donor.user.full_name if donor.user else None,
            email=donor.user.email if donor.user else None,
        )

    def list_donors(
        self,
        blood_group: Optional[BloodGroup],
        city: Optional[str],
        search: Optional[str],
        page: int,
        page_size: int,
    ) -> PaginatedDonors:
        skip = (page - 1) * page_size
        donors, total = self.repo.get_all(blood_group, city, search, skip, page_size)

        donor_out_list = [
            DonorOut(
                id=d.id,
                user_id=d.user_id,
                blood_group=d.blood_group,
                phone=d.phone,
                city=d.city,
                address=d.address,
                last_donation_date=d.last_donation_date,
                is_available=d.is_available,
                full_name=d.user.full_name if d.user else None,
                email=d.user.email if d.user else None,
            )
            for d in donors
        ]

        return PaginatedDonors.build(
            donors=donor_out_list,
            total=total,
            page=page,
            page_size=page_size,
        )

    def update_profile(self, donor_id: int, data: DonorUpdate, current_user: User) -> Donor:
        donor = self.repo.get_by_id(donor_id)
        if not donor:
            raise NotFoundException("Donor not found")
        if donor.user_id != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenException("You can only update your own profile")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(donor, field, value)

        return self.repo.update(donor)

    def update_availability(
        self, donor_id: int, data: AvailabilityUpdate, current_user: User
    ) -> Donor:
        donor = self.repo.get_by_id(donor_id)
        if not donor:
            raise NotFoundException("Donor not found")
        if donor.user_id != current_user.id and current_user.role != UserRole.admin:
            raise ForbiddenException("Access denied")

        donor.is_available = data.is_available
        return self.repo.update(donor)