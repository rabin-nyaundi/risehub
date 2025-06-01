from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    posts,
    accounts,
    # campaigns,
    analytics,
    scheduling,
    webhooks
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["social accounts"])
# api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(scheduling.router, prefix="/scheduling", tags=["scheduling"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
