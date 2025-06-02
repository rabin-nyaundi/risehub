from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserResponse, UserUpdateSchema
from app.db.repositories.user_repo import UserRepository
from app.db.session import DatabaseSession

class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            return repo.get(db, user_id)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            return repo.get_by_username(db, email)  # Using username field for email

    @staticmethod
    async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            return repo.get_all(db, skip, limit)

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdateSchema) -> dict:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            user = repo.get(db, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Update user and profile
            update_data = user_data.dict(exclude_unset=True)
            updated_user = repo.update(db, user_id, **update_data)
            
            if not updated_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user"
                )
            
            user_dict = {
                "id": updated_user.id,
                "email": updated_user.email,
                "username": updated_user.username,
                "is_active": updated_user.is_active,
                "created_at": updated_user.created_at,
                "updated_at": updated_user.updated_at,
                "profile": {
                    "user_id": updated_user.profile.user_id,
                    "bio": updated_user.profile.bio,
                    "full_name": updated_user.profile.full_name,
                    "location": updated_user.profile.location,
                    "profile_picture": updated_user.profile.profile_picture,
                    "created_at": updated_user.profile.created_at,
                    "updated_at": updated_user.profile.updated_at,
                    "is_deleted": updated_user.profile.is_deleted,
                    "deleted_at": updated_user.profile.deleted_at
                } if updated_user.profile else None,
                "roles": [
                    {
                        "id": role.id,
                        "name": role.name,
                        "description": role.description,
                        "created_at": role.created_at,
                        "updated_at": role.updated_at,
                        "is_deleted": role.is_deleted,
                        "deleted_at": role.deleted_at
                    }
                    for role in updated_user.roles
                ] if updated_user.roles else []
            }
            
            return user_dict

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            user = repo.get(db, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return repo.delete(db, user_id)

    @staticmethod
    async def get_user_teams(user_id: int) -> List:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            user = repo.get_with_roles(db, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user.roles

    @staticmethod
    async def get_user_social_accounts(user_id: int) -> List:
        with DatabaseSession() as db:
            from app.db.repositories.account_repo import AccountRepository
            repo = AccountRepository(db)
            return repo.get_by_user(db, user_id) 