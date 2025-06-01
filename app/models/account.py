from enums import PlatformType
from sqlalchemy import Column, String, ForeignKey, Enum, Text, DateTime, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import BaseModel
from app.models.post import post_social_accounts


class SocialAccount(BaseModel):
    __tablename__ = "social_accounts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    platform = Column(Enum(PlatformType), nullable=False)
    platform_user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    profile_data = Column(JSON)    
    
    user = relationship("User", back_populates="social_accounts")
    posts = relationship("Post", secondary=post_social_accounts, back_populates="social_accounts")
    
    def __repr__(self):
        return f"<SocialAccount(id={self.id}, platform={self.platform}, username='{self.username}')>"   