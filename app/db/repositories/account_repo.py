from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.account import SocialAccount
from enums import PlatformType

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[SocialAccount]:
        return self.db.query(SocialAccount).filter(SocialAccount.id == id).first()

    def get_by_user_id(self, user_id: int) -> List[SocialAccount]:
        return self.db.query(SocialAccount).filter(SocialAccount.user_id == user_id).all()

    def get_by_platform_and_user(self, platform: str, user_id: int) -> Optional[SocialAccount]:
        return self.db.query(SocialAccount).filter(
            SocialAccount.platform == platform,
            SocialAccount.user_id == user_id
        ).first()

    def create(self, **kwargs) -> SocialAccount:
        account = SocialAccount(**kwargs)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, id: int, **kwargs) -> Optional[SocialAccount]:
        account = self.get_by_id(id)
        if account:
            for key, value in kwargs.items():
                setattr(account, key, value)
            self.db.commit()
            self.db.refresh(account)
        return account

    def delete(self, id: int) -> bool:
        account = self.get_by_id(id)
        if account:
            self.db.delete(account)
            self.db.commit()
            return True
        return False

    def get_by_user(self, db: Session, user_id: UUID) -> List[SocialAccount]:
        return db.query(SocialAccount).filter(
            SocialAccount.user_id == user_id,
            SocialAccount.is_deleted == False
        ).all()

    def get_by_platform(self, db: Session, user_id: UUID, platform: PlatformType) -> Optional[SocialAccount]:
        return db.query(SocialAccount).filter(
            SocialAccount.user_id == user_id,
            SocialAccount.platform == platform,
            SocialAccount.is_deleted == False
        ).first()

    def get_active_accounts(self, db: Session, user_id: UUID) -> List[SocialAccount]:
        return db.query(SocialAccount).filter(
            SocialAccount.user_id == user_id,
            SocialAccount.is_active == True,
            SocialAccount.is_deleted == False
        ).all()

    def update_token(self, db: Session, account_id: UUID, access_token: str, refresh_token: Optional[str] = None) -> Optional[SocialAccount]:
        account = self.get_by_id(account_id)
        if not account:
            return None
        
        account.access_token = access_token
        if refresh_token:
            account.refresh_token = refresh_token
        
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_engagement_metrics(self, db: Session, account_id: UUID, followers: int, following: int, posts: int, engagement_rate: float) -> Optional[SocialAccount]:
        account = self.get_by_id(account_id)
        if not account:
            return None
        
        account.followers_count = followers
        account.following_count = following
        account.posts_count = posts
        account.engagement_rate = engagement_rate
        
        self.db.commit()
        self.db.refresh(account)
        return account 