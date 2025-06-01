"""
Core module initialization file.
This module exports security-related functions for password hashing, verification,
and JWT token management.
"""

from .security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    pwd_context
)

from .dependencies import get_current_superuser, get_current_active_user

__all__ = [
    # Password management
    'verify_password',
    'get_password_hash',
    'pwd_context',
    
    # JWT token management
    'create_access_token',
    'verify_token',
    
    # User authentication
    'get_current_superuser',
    'get_current_active_user'
]
