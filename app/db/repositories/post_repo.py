from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.models.post import Post
from app.db.repositories.base import BaseRepository
from enums import PostStatus

class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post)

    def get_by_user(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).filter(
            Post.user_id == user_id,
            Post.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_scheduled_posts(self, db: Session, user_id: UUID) -> List[Post]:
        return db.query(Post).filter(
            Post.user_id == user_id,
            Post.status == PostStatus.SCHEDULED,
            Post.is_deleted == False
        ).all()

    def get_published_posts(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).filter(
            Post.user_id == user_id,
            Post.status == PostStatus.PUBLISHED,
            Post.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_draft_posts(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).filter(
            Post.user_id == user_id,
            Post.status == PostStatus.DRAFT,
            Post.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_posts_to_publish(self, db: Session) -> List[Post]:
        now = datetime.utcnow()
        return db.query(Post).filter(
            Post.status == PostStatus.SCHEDULED,
            Post.schedule_time <= now,
            Post.is_deleted == False
        ).all()

    def update_post_status(self, db: Session, post_id: UUID, status: PostStatus) -> Optional[Post]:
        post = self.get(db, post_id)
        if not post:
            return None
        
        post.status = status
        if status == PostStatus.PUBLISHED:
            post.posted_at = datetime.utcnow()
        
        db.commit()
        db.refresh(post)
        return post 