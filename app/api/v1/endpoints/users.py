from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core import get_current_active_user, get_current_superuser
from app.models.user import User
from app.schemas import UserResponse, UserUpdateSchema
from app.services.user_service import UserService

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_in: UserUpdateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user
    """
    user = await UserService.update_user(current_user.id, user_in)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific user by id
    """
    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Retrieve users
    """
    users = await UserService.get_users(skip=skip, limit=limit)
    return users

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Delete a user
    """
    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    await UserService.delete_user(user_id)
    return user

@router.get("/me/teams", response_model=List[Any])
async def read_user_teams(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's teams
    """
    teams = await UserService.get_user_teams(current_user.id)
    return teams

@router.get("/me/accounts", response_model=List[Any])
async def read_user_social_accounts(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's social accounts
    """
    accounts = await UserService.get_user_social_accounts(current_user.id)
    return accounts
