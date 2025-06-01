from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core import get_current_active_user
from app.models.user import User
from app.schemas import PostResponse, PostUpdateSchema, PostCreate
from app.services.post_service import PostService

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(
    post_in: PostCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new post
    """
    post = await PostService.create_post(post_in, current_user.id)
    return post

@router.get("/{post_id}", response_model=PostResponse)
async def read_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get post by ID
    """
    post = await PostService.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return post

@router.get("/", response_model=List[PostResponse])
async def read_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve posts
    """
    posts = await PostService.get_user_posts(current_user.id, skip=skip, limit=limit)
    return posts

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update post
    """
    post = await PostService.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    post = await PostService.update_post(post_id, post_in)
    return post

@router.delete("/{post_id}", response_model=PostResponse)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete post
    """
    post = await PostService.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    await PostService.delete_post(post_id)
    return post

@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Publish post to social media
    """
    post = await PostService.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    post = await PostService.publish_post(post_id)
    return post
