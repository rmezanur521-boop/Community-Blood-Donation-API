from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.schemas.auth import TokenResponse
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import ConflictException, UnauthorizedException


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserCreate) -> User:
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ConflictException("Email already registered")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        return self.repo.create(user)

    def login(self, data: UserLogin) -> TokenResponse:
        user = self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")

        token = create_access_token({"sub": str(user.id), "role": user.role.value})
        return TokenResponse(access_token=token)