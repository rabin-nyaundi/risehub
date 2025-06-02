import os
from typing import Optional, List, Union
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from pydantic import field_validator

# Get the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str
    DEBUG: bool
    API_PREFIX: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    ALGORITHM: str

    # Database Connection Settings
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int
    DATABASE_MAX_OVERFLOW: int

    # Redis Configuration
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: Optional[str] = None

    # RabbitMQ Settings
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str

    # Social Media API Keys
    # FACEBOOK_APP_ID: str
    # FACEBOOK_APP_SECRET: str
    # FACEBOOK_REDIRECT_URI: str
    # TWITTER_API_KEY: str
    # TWITTER_API_SECRET: str
    # TWITTER_ACCESS_SECRET: str
    # INSTAGRAM_CLIENT_ID: str
    # INSTAGRAM_CLIENT_SECRET: str
    # LINKEDIN_CLIENT_ID: str
    # LINKEDIN_CLIENT_SECRET: str
    # LINKEDIN_REDIRECT_URI: str
    # TIKTOK_CLIENT_KEY: str
    # TIKTOK_CLIENT_SECRET: str
    # TIKTOK_REDIRECT_URI: str

    # Email Settings
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str

    # AWS Settings
    # AWS_ACCESS_KEY_ID: str
    # AWS_SECRET_ACCESS_KEY: str
    # AWS_REGION: str
    # AWS_BUCKET_NAME: str

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_PERIOD: int
    
    ALLOWED_ORIGINS: Union[str, List[str]]
    ALLOWED_HOSTS: Union[str, List[str]]

    @field_validator("ALLOWED_ORIGINS", "ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_list(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    class Config:
        env_file = str(ROOT_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
