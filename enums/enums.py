from enum import Enum

class PyEnum(Enum):
    def __str__(self):
        return self.value


class UserType(PyEnum):
    INFLUENCER = "influencer"
    BRAND_OWNER = "brand_owner"
    ADMIN = "admin"

class PlatformType(PyEnum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    THREADS = "threads"

class PostStatus(PyEnum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class ContractStatus(PyEnum):
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"