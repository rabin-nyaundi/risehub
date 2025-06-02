from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from app.models.user import User, Profile, Role

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    
    def get_active_by_id(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id, User.is_deleted == False, User.is_active == True).first()

    def get(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).options(
            joinedload(User.profile),
            joinedload(User.roles)
        ).filter(User.id == user_id, User.is_deleted == False).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.is_deleted == False).offset(skip).limit(limit).all()

    def create(self, db: Session, **kwargs) -> User:
        user = User(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user_id: UUID, **kwargs) -> Optional[User]:
        user = self.get(db, user_id)
        if user:
            profile_data = kwargs.pop('profile', None)
            
            for key, value in kwargs.items():
                setattr(user, key, value)
            
            if profile_data:
                if not user.profile:
                    profile = Profile(user=user, **profile_data)
                    db.add(profile)
                else:
                    for key, value in profile_data.items():
                        setattr(user.profile, key, value)
            
            db.commit()
            db.refresh(user)
            user.profile
            user.roles
            
        return user

    def delete(self, db: Session, user_id: UUID) -> bool:
        user = self.get(db, user_id)
        if user:
            user.is_deleted = True
            db.commit()
            return True
        return False

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username, User.is_deleted == False).first()

    def get_with_profile(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    def get_with_roles(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    def create_with_profile(self, db: Session, user_data: dict, profile_data: dict) -> User:
        user = User(**user_data)
        profile = Profile(**profile_data, user=user)
        db.add(user)
        db.add(profile)
        db.commit()
        db.refresh(user)
        return user

    def add_role(self, db: Session, user_id: UUID, role_id: UUID) -> bool:
        user = self.get(db, user_id)
        role = db.query(Role).filter(Role.id == role_id).first()
        if not user or not role:
            return False
        
        if role not in user.roles:
            user.roles.append(role)
            db.commit()
        return True

    def remove_role(self, db: Session, user_id: UUID, role_id: UUID) -> bool:
        user = self.get(db, user_id)
        role = db.query(Role).filter(Role.id == role_id).first()
        if not user or not role:
            return False
        
        if role in user.roles:
            user.roles.remove(role)
            db.commit()
        return True

    def create_profile(self, db: Session, user_id: UUID, **profile_data) -> Optional[Profile]:
        user = self.get(db, user_id)
        if not user:
            return None
            
        profile = Profile(**profile_data, user=user)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile 