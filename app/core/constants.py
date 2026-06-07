class BloodGroupLabels:
    ALL_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


class RoleLabels:
    ADMIN = "admin"
    DONOR = "donor"
    REQUESTER = "requester"


class RequestStatusLabels:
    PENDING = "pending"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


class PaginationDefaults:
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100