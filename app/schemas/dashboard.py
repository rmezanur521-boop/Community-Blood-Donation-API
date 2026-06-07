from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_donors: int
    available_donors: int
    active_requests: int
    total_users: int
    fulfilled_requests: int