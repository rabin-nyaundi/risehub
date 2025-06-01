from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

from app.models.post import Post
from app.models.account import SocialAccount

class SocialPlatformBase(ABC):
    def __init__(self, account: SocialAccount):
        self.account = account
        self.api_client = self._initialize_api_client()

    @abstractmethod
    def _initialize_api_client(self) -> Any:
        """Initialize the platform-specific API client."""
        pass

    @abstractmethod
    async def publish_post(self, post: Post) -> Dict[str, Any]:
        """Publish a post to the social platform."""
        pass

    @abstractmethod
    async def delete_post(self, platform_post_id: str) -> bool:
        """Delete a post from the social platform."""
        pass

    @abstractmethod
    async def get_post_analytics(self, platform_post_id: str) -> Dict[str, Any]:
        """Get analytics for a specific post."""
        pass

    @abstractmethod
    async def get_account_analytics(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get analytics for the connected account."""
        pass

    @abstractmethod
    async def validate_credentials(self) -> bool:
        """Validate the platform credentials."""
        pass

    @abstractmethod
    async def refresh_token(self) -> bool:
        """Refresh the platform access token."""
        pass

    @staticmethod
    def get_platform_handler(platform: str) -> 'SocialPlatformBase':
        """Factory method to get the appropriate platform handler."""
        platform_handlers = {
            'instagram': InstagramPlatform,
            'twitter': TwitterPlatform,
            'facebook': FacebookPlatform,
            'linkedin': LinkedInPlatform,
            'tiktok': TikTokPlatform
        }
        
        handler_class = platform_handlers.get(platform.lower())
        if not handler_class:
            raise ValueError(f"Unsupported platform: {platform}")
            
        return handler_class

    @abstractmethod
    async def get_media_upload_url(self, media_type: str) -> str:
        """Get a URL for media upload."""
        pass

    @abstractmethod
    async def get_user_profile(self) -> Dict[str, Any]:
        """Get the user's profile information."""
        pass

    @abstractmethod
    async def get_available_audiences(self) -> List[Dict[str, Any]]:
        """Get available targeting audiences."""
        pass

    @abstractmethod
    async def validate_post_content(self, content: str) -> bool:
        """Validate post content against platform guidelines."""
        pass

# Alias for backward compatibility
SocialPlatform = SocialPlatformBase 