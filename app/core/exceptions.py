from fastapi import HTTPException, status

class SocialAccountException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class AccountConnectionError(SocialAccountException):
    def __init__(self, platform: str):
        super().__init__(
            detail=f"Failed to connect to {platform} account"
        )

class InvalidCredentialsError(SocialAccountException):
    def __init__(self, platform: str):
        super().__init__(
            detail=f"Invalid credentials for {platform} account"
        )

class RateLimitExceededError(SocialAccountException):
    def __init__(self, platform: str):
        super().__init__(
            detail=f"Rate limit exceeded for {platform} API"
        )

class PostSchedulingError(SocialAccountException):
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Failed to schedule post: {detail}"
        )

class AnalyticsError(SocialAccountException):
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Analytics error: {detail}"
        )
