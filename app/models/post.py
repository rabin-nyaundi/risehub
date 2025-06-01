from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, DateTime, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.models.base import BaseModel

# Association table for many-to-many relationship between posts and social accounts
post_social_accounts = Table(
    'post_social_accounts',
    BaseModel.metadata,
    Column('post_id', UUID(as_uuid=True), ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('social_account_id', String, ForeignKey('social_accounts.id', ondelete='CASCADE'), primary_key=True)
)

class Post(BaseModel):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    content = Column(Text, nullable=False)
    media_url = Column(Text)
    platforms = Column(ARRAY(String(20)), nullable=False)
    schedule_time = Column(DateTime, index=True)
    status = Column(String(20), default="draft")
    posted_at = Column(DateTime)
    post_ids = Column(JSONB, default=dict)
    
    user = relationship("User", back_populates="posts")
    social_accounts = relationship("SocialAccount", secondary=post_social_accounts, back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, content='{self.content[:50]}...')>"    