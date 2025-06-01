from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.config.settings import settings
from app.models.user import User, Profile, Role
from app.schemas import UserCreateSchema, UserLoginSchema, UserResponse
from app.services.user_service import UserService
from app.db.session import DatabaseSession
from app.db.repositories.user_repo import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            user = repo.get_by_username(db, email)
            if not user:
                return None
            if not AuthService.verify_password(password, user.password_hash):
                return None
            return user

    @staticmethod
    async def create_user(user_data: UserCreateSchema) -> UserResponse:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            hashed_password = AuthService.get_password_hash(user_data.password)
            
            # Create user with basic info
            user = repo.create(db,                
                email=user_data.email,
                password_hash=hashed_password,
                username=user_data.username,
                is_active=True
            )
            
            # Create profile for the user
            profile = Profile(user=user)
            db.add(profile)
            
            # Add default user role if it exists
            default_role = db.query(Role).filter(Role.name == "user").first()
            if default_role:
                user.roles.append(default_role)
            
            db.commit()
            db.refresh(user)
            
            # Load all relationships before closing the session
            user.profile
            user.roles

            return UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                profile=user.profile,
                roles=user.roles
            ) 