from typing import Any, Optional


def success_response(
    data: Any,
    message: str = "Success",
    status_code: int = 200,
) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code,
    }


def error_response(
    message: str,
    status_code: int = 400,
    detail: Optional[Any] = None,
) -> dict:
    return {
        "success": False,
        "message": message,
        "detail": detail,
        "status_code": status_code,
    }