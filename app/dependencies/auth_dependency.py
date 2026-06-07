from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    user = UserRepository(db).get_by_id(int(user_id))
    if not user:
        raise UnauthorizedException("User not found")

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise ForbiddenException("Admin access required")
    return current_user


def require_donor(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.donor, UserRole.admin]:
        raise ForbiddenException("Donor access required")
    return current_user


def require_requester(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.requester, UserRole.admin]:
        raise ForbiddenException("Requester access required")
    return current_user