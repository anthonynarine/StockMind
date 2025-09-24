from fastapi import APIRouter
from app.users.deps import fastapi_users, auth_backend
from app.users.schemas import UserRead, UserCreate

router = APIRouter()

"""
🔐 Authentication Routes for FastAPI Users

This module registers the following routes:

- POST   /auth/jwt/login          (Login via JWT, returns access/refresh tokens)
- POST   /auth/register           (Create a new user account)
- POST   /auth/forgot-password    (Request a password reset token)
- POST   /auth/reset-password     (Reset password using token)
- GET    /users/me                (Get current logged-in user's profile)
- GET    /users/{id}              (Get a specific user's profile by ID)

All routes are handled by FastAPI Users using the configured `auth_backend`.
"""

# ✅ JWT Login Route
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# ✅ Registration Route
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# ✅ Forgot & Reset Password Routes
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# ✅ User Profile Routes (/me and /{id})
router.include_router(
    fastapi_users.get_users_router(UserRead, UserRead),
    prefix="/users",
    tags=["users"],
)
