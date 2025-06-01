from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from app.models.post import Post
from app.schemas.post import PostSchedule
from app.services.post_service import PostService

class SchedulingService:
    @staticmethod
    async def schedule_post(post_id: int, schedule_data: PostSchedule) -> Post:
        post = await PostService.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Validate scheduled time
        if schedule_data.scheduled_time < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scheduled time must be in the future"
            )
        
        post.scheduled_time = schedule_data.scheduled_time
        post.status = "scheduled"
        # TODO: Update post in database
        
        return post

    @staticmethod
    async def get_scheduled_posts(
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Post]:
        if not start_time:
            start_time = datetime.utcnow()
        if not end_time:
            end_time = start_time + timedelta(days=7)
            
        # TODO: Implement actual database query for scheduled posts
        return []

    @staticmethod
    async def cancel_scheduled_post(post_id: int) -> Post:
        post = await PostService.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if post.status != "scheduled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post is not scheduled"
            )
        
        post.status = "draft"
        post.scheduled_time = None
        # TODO: Update post in database
        
        return post

    @staticmethod
    async def reschedule_post(post_id: int, new_schedule: PostSchedule) -> Post:
        post = await PostService.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if post.status != "scheduled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post is not scheduled"
            )
        
        # Validate new scheduled time
        if new_schedule.scheduled_time < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New scheduled time must be in the future"
            )
        
        post.scheduled_time = new_schedule.scheduled_time
        # TODO: Update post in database
        
        return post

    @staticmethod
    async def get_upcoming_posts(limit: int = 10) -> List[Post]:
        # TODO: Implement actual database query for upcoming posts
        return [] 