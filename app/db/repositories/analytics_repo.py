from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from uuid import UUID
from datetime import datetime, timedelta
from app.models.post import Post
from app.models.account import SocialAccount
from enums import PlatformType

class AnalyticsRepository:
    def get_user_engagement_stats(self, db: Session, user_id: UUID, days: int = 30) -> Dict[str, Any]:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get total posts
        total_posts = db.query(func.count(Post.id)).filter(
            Post.user_id == user_id,
            Post.is_deleted == False,
            Post.posted_at >= start_date
        ).scalar()

        # Get posts by platform
        posts_by_platform = db.query(
            Post.platforms,
            func.count(Post.id)
        ).filter(
            Post.user_id == user_id,
            Post.is_deleted == False,
            Post.posted_at >= start_date
        ).group_by(Post.platforms).all()

        # Get average engagement rate
        avg_engagement = db.query(
            func.avg(SocialAccount.engagement_rate)
        ).filter(
            SocialAccount.user_id == user_id,
            SocialAccount.is_deleted == False
        ).scalar() or 0.0

        return {
            "total_posts": total_posts,
            "posts_by_platform": dict(posts_by_platform),
            "average_engagement_rate": float(avg_engagement)
        }

    def get_platform_performance(self, db: Session, user_id: UUID, platform: PlatformType, days: int = 30) -> Dict[str, Any]:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get posts for platform
        posts = db.query(Post).filter(
            Post.user_id == user_id,
            Post.platforms.contains([platform]),
            Post.is_deleted == False,
            Post.posted_at >= start_date
        ).all()

        # Get account stats
        account = db.query(SocialAccount).filter(
            SocialAccount.user_id == user_id,
            SocialAccount.platform == platform,
            SocialAccount.is_deleted == False
        ).first()

        return {
            "total_posts": len(posts),
            "followers_count": account.followers_count if account else 0,
            "following_count": account.following_count if account else 0,
            "engagement_rate": account.engagement_rate if account else 0.0
        }

    def get_best_posting_times(self, db: Session, user_id: UUID, platform: PlatformType) -> List[Dict[str, Any]]:
        # Get posts with engagement data
        posts = db.query(Post).filter(
            Post.user_id == user_id,
            Post.platforms.contains([platform]),
            Post.is_deleted == False,
            Post.posted_at.isnot(None)
        ).order_by(desc(Post.posted_at)).all()

        # Group posts by hour and calculate average engagement
        hourly_stats = {}
        for post in posts:
            hour = post.posted_at.hour
            if hour not in hourly_stats:
                hourly_stats[hour] = {"count": 0, "total_engagement": 0}
            
            hourly_stats[hour]["count"] += 1
            # Assuming post_ids contains engagement data
            engagement = sum(float(v) for v in post.post_ids.values()) if post.post_ids else 0
            hourly_stats[hour]["total_engagement"] += engagement

        # Calculate averages and sort by engagement
        best_times = []
        for hour, stats in hourly_stats.items():
            if stats["count"] > 0:
                avg_engagement = stats["total_engagement"] / stats["count"]
                best_times.append({
                    "hour": hour,
                    "average_engagement": avg_engagement,
                    "post_count": stats["count"]
                })

        return sorted(best_times, key=lambda x: x["average_engagement"], reverse=True) 