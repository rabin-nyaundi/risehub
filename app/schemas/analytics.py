from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID


class AnalyticsFilter(BaseModel):
    start_date: datetime
    end_date: datetime
    platform: Optional[str] = None
    post_id: Optional[UUID] = None
    account_id: Optional[UUID] = None


class AnalyticsResponse(BaseModel):
    total_posts: int
    total_engagement: int
    total_reach: int
    total_impressions: int
    engagement_rate: float
    platform_breakdown: Dict[str, Dict[str, Any]]
    post_analytics: List[Dict[str, Any]]
    account_analytics: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 