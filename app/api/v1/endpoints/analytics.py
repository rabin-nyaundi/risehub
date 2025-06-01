from typing import Any, List, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from app.core import get_current_active_user
from app.models.user import User
from app.schemas.analytics import AnalyticsFilter, AnalyticsResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/posts/{post_id}", response_model=AnalyticsResponse)
async def get_post_analytics(
    post_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get analytics for a specific post
    """
    analytics = await AnalyticsService.get_post_analytics(
        post_id=post_id,
        start_date=start_date,
        end_date=end_date
    )
    return analytics

@router.get("/user", response_model=List[AnalyticsResponse])
async def get_user_analytics(
    filter_data: AnalyticsFilter,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get analytics for the current user
    """
    analytics = await AnalyticsService.get_user_analytics(
        user_id=current_user.id,
        filter_data=filter_data
    )
    return analytics

@router.get("/platform/{platform}", response_model=Dict[str, Any])
async def get_platform_analytics(
    platform: str,
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get analytics for a specific platform
    """
    analytics = await AnalyticsService.get_platform_analytics(
        platform=platform,
        start_date=start_date,
        end_date=end_date
    )
    return analytics

@router.get("/campaigns/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign_analytics(
    campaign_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get analytics for a specific campaign
    """
    analytics = await AnalyticsService.get_campaign_analytics(
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date
    )
    return analytics

@router.post("/reports/generate", response_model=Dict[str, Any])
async def generate_analytics_report(
    report_type: str,
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Generate an analytics report
    """
    report = await AnalyticsService.generate_analytics_report(
        user_id=current_user.id,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date
    )
    return report 