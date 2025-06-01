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
    async def update_user(user_id: int, user_data: UserUpdateSchema) -> User:
        with DatabaseSession() as db:
            repo = UserRepository(db)
            user = repo.get(db, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Update user fields
            update_data = user_data.dict(exclude_unset=True)
            updated_user = repo.update(db, user_id, **update_data)
            if not updated_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user"
                )
            return updated_user

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