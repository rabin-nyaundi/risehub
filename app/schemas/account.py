from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID


class SocialAccountBase(BaseModel):
    platform: str
    platform_user_id: str
    username: str
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    profile_data: Optional[Dict] = None


class SocialAccountCreate(SocialAccountBase):
    pass


class SocialAccountUpdate(BaseModel):
    platform: Optional[str] = None
    platform_user_id: Optional[str] = None
    username: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    profile_data: Optional[Dict] = None


class SocialAccountSchema(SocialAccountBase):
    id: UUID
    user_id: UUID
    is_active: bool
    followers_count: int
    following_count: int
    posts_count: int
    engagement_rate: float
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


class SocialAccountResponse(SocialAccountSchema):
    pass