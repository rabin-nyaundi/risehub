from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID

class PostSchedule(BaseModel):
    post_id: UUID
    schedule_time: datetime
    repeat: Optional[str] = None  # e.g., 'daily', 'weekly'
    is_active: bool = True

class PostBase(BaseModel):
    content: str
    media_url: Optional[str] = None
    platforms: List[str]
    schedule_time: Optional[datetime] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    content: Optional[str] = None
    platforms: Optional[List[str]] = None

class PostSchema(PostBase):
    id: UUID
    user_id: UUID
    status: str
    posted_at: Optional[datetime]
    post_ids: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class PostResponse(PostSchema):
    pass

class PostUpdateSchema(PostBase):
    pass
