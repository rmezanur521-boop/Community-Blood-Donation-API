from pydantic import BaseModel
from typing import Any, Optional


class MessageResponse(BaseModel):
    message: str


class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, total: int, page: int, page_size: int) -> "PaginationMeta":
        import math
        return cls(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if page_size > 0 else 0,
        )