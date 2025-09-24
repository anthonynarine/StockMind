from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from uuid import UUID

from app.users.models import User
from app.users.schemas import UserCreate, UserRead
from app.users.manager import get_user_manager, SECRET

# -------------------------------------------------------
# 🔐 Bearer Transport (Authorization: Bearer <token>)
# -------------------------------------------------------

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# -------------------------------------------------------
# 🔐 JWT Strategy for access tokens
# -------------------------------------------------------

def get_jwt_strategy() -> JWTStrategy:
    """
    Returns the configured JWT strategy using your app's secret key.

    Returns:
        JWTStrategy: Configured JWT strategy instance.
    """
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# -------------------------------------------------------
# 🔐 Authentication Backend (JWT + Bearer)
# -------------------------------------------------------

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# -------------------------------------------------------
# ✅ FastAPIUsers instance (v12+ API)
# Provides:
# - Routers (login, register, etc.)
# - User management
# - Current user dependencies
# -------------------------------------------------------

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

# -------------------------------------------------------
# 🔐 Dependency to protect routes (e.g., /portfolio)
# -------------------------------------------------------

current_active_user = fastapi_users.current_user(active=True)
