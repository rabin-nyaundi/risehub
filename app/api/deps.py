# from typing import Generator, Optional
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jwt import decode, PyJWTError
# from pydantic import ValidationError

# from app.config.settings import settings
# from app.core.security import ALGORITHM
# from app.models.user import User
# from app.services.auth_service import AuthService
# from app.services.user_service import UserService

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

# async def get_current_user(
#     token: str = Depends(oauth2_scheme)
# ) -> User:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[ALGORITHM]
#         )
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except (PyJWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     user = await UserService.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return user

# async def get_current_active_user(
#     current_user: User = Depends(get_current_user),
# ) -> User:
#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Inactive user"
#         )
#     return current_user

# async def get_current_superuser(
#     current_user: User = Depends(get_current_user),
# ) -> User:
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="The user doesn't have enough privileges"
#         )
#     return current_user 