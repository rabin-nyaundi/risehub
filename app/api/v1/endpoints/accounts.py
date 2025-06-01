from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.account import SocialAccount
from app.schemas.account import (
    SocialAccountCreate,
    SocialAccountResponse,
    SocialAccountUpdate
)
from app.services.social_platforms.base import SocialPlatform
from app.core.exceptions import AccountConnectionError, InvalidCredentialsError
from app.db.repositories.account_repo import AccountRepository

router = APIRouter()

@router.post("/", response_model=SocialAccountResponse)
async def connect_social_account(
    account_data: SocialAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Connect a new social media account"""
    account_repo = AccountRepository(db)
    
    # Check if account already exists
    existing_account = account_repo.get_by_platform_and_user(
        platform=account_data.platform,
        user_id=current_user.id
    )
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account already connected for {account_data.platform}"
        )
    
    # Initialize platform-specific handler
    platform = SocialPlatform.get_platform(account_data.platform)
    
    try:
        # Verify credentials with platform
        platform.verify_credentials(
            access_token=account_data.access_token,
            refresh_token=account_data.refresh_token
        )
        
        # Create account in database
        account = account_repo.create(
            user_id=current_user.id,
            platform=account_data.platform,
            access_token=account_data.access_token,
            refresh_token=account_data.refresh_token,
            platform_user_id=account_data.platform_user_id
        )
        
        return account
    except Exception as e:
        raise AccountConnectionError(account_data.platform)

@router.get("/", response_model=List[SocialAccountResponse])
async def list_social_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all connected social media accounts"""
    account_repo = AccountRepository(db)
    return account_repo.get_by_user_id(current_user.id)

@router.get("/{account_id}", response_model=SocialAccountResponse)
async def get_social_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get details of a specific social media account"""
    account_repo = AccountRepository(db)
    account = account_repo.get_by_id(account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return account

@router.put("/{account_id}", response_model=SocialAccountResponse)
async def update_social_account(
    account_id: int,
    account_data: SocialAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update social media account credentials"""
    account_repo = AccountRepository(db)
    account = account_repo.get_by_id(account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Verify new credentials
    platform = SocialPlatform.get_platform(account.platform)
    try:
        platform.verify_credentials(
            access_token=account_data.access_token,
            refresh_token=account_data.refresh_token
        )
    except Exception:
        raise InvalidCredentialsError(account.platform)
    
    # Update account
    updated_account = account_repo.update(
        id=account_id,
        access_token=account_data.access_token,
        refresh_token=account_data.refresh_token
    )
    
    return updated_account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_social_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Disconnect a social media account"""
    account_repo = AccountRepository(db)
    account = account_repo.get_by_id(account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    account_repo.delete(account_id)
    return None
