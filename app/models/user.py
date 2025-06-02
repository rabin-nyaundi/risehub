from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    profile = relationship("Profile", uselist=False, back_populates="user")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    # Relationships
    posts = relationship("Post", back_populates="user")
    social_accounts = relationship("SocialAccount", back_populates="user")

class Profile(BaseModel):
    __tablename__ = "profiles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    bio = Column(Text)
    full_name = Column(String(100))
    location = Column(String(100), index=True)
    profile_picture = Column(Text)
    user = relationship("User", back_populates="profile")

class Role(BaseModel):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

class Permission(BaseModel):
    __tablename__ = "permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")

class RolePermission(BaseModel):
    __tablename__ = "role_permissions"
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

class UserRole(BaseModel):
    __tablename__ = "user_roles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
