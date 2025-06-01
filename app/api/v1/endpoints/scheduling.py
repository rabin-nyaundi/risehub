from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from app.core import get_current_active_user
from app.models.user import User
from app.schemas.post import PostSchedule, PostResponse
from app.services.scheduling_service import SchedulingService

router = APIRouter()

@router.post("/{post_id}/schedule", response_model=PostResponse)
async def schedule_post(
    post_id: int,
    schedule_in: PostSchedule,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Schedule a post for future publishing
    """
    post = await SchedulingService.schedule_post(post_id, schedule_in)
    return post

@router.get("/scheduled", response_model=List[PostResponse])
async def read_scheduled_posts(
    start_time: datetime = None,
    end_time: datetime = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get scheduled posts
    """
    posts = await SchedulingService.get_scheduled_posts(
        start_time=start_time,
        end_time=end_time
    )
    return posts

@router.post("/{post_id}/cancel", response_model=PostResponse)
async def cancel_scheduled_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Cancel a scheduled post
    """
    post = await SchedulingService.cancel_scheduled_post(post_id)
    return post

@router.post("/{post_id}/reschedule", response_model=PostResponse)
async def reschedule_post(
    post_id: int,
    schedule_in: PostSchedule,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Reschedule a post
    """
    post = await SchedulingService.reschedule_post(post_id, schedule_in)
    return post

@router.get("/upcoming", response_model=List[PostResponse])
async def read_upcoming_posts(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get upcoming posts
    """
    posts = await SchedulingService.get_upcoming_posts(limit=limit)
    return posts 