from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class ProfileSchema(BaseModel):
    user_id: UUID
    bio: Optional[str]
    full_name: Optional[str]
    location: Optional[str]
    profile_picture: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class RoleSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class PermissionSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: UUID
    username: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]
    profile: Optional[ProfileSchema]
    roles: List[RoleSchema]

    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    username:str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile: Optional[ProfileSchema]
    roles: List[RoleSchema]

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    profile: Optional[dict] = None

    class Config:
        from_attributes = True