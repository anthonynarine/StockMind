from fastapi import Depends, Request
from fastapi_users.manager import BaseUserManager
from fastapi_users.exceptions import UserAlreadyExists
from app.users.db import get_user_db
from app.users.models import User
from uuid import UUID
from typing import AsyncGenerator

# 🔐 Secret key for JWT operations (should come from env var in production)
SECRET = "SUPER_SECRET_JWT_KEY"


class UserManager(BaseUserManager[User, UUID]):
    """
    Custom user manager for FastAPI Users.

    Handles user lifecycle logic such as registration, password reset,
    verification, and token decoding for UUID-based primary keys.
    """

    user_db_model = User  # ✅ Required: link to the SQLAlchemy User model
    reset_password_token_secret = SECRET  # 🔐 Used to sign password reset tokens
    verification_token_secret = SECRET    # 🔐 Used to sign email verification tokens

    def parse_id(self, user_id: str) -> UUID:
        """
        Convert user_id from JWT (as string) into UUID format.

        Required for proper functioning when using UUID primary keys.

        Args:
            user_id (str): User ID extracted from token.

        Returns:
            UUID: Parsed UUID instance.
        """
        return UUID(user_id)

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        """
        Optional hook: triggered after a user successfully registers.

        Args:
            user (User): The registered user object.
            request (Request, optional): The HTTP request context.
        """
        print(f"✅ User registered: {user.email}")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None) -> None:
        """
        Optional hook: triggered after a user requests a password reset.

        Args:
            user (User): The user requesting the reset.
            token (str): The generated reset token.
            request (Request, optional): The HTTP request context.
        """
        print(f"🔐 Forgot password requested for {user.email}")
        print(f"🔗 Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None) -> None:
        """
        Optional hook: triggered after a user requests email verification.

        Args:
            user (User): The user requesting verification.
            token (str): The generated verification token.
            request (Request, optional): The HTTP request context.
        """
        print(f"📧 Verification requested for {user.email}")
        print(f"🔗 Verification token: {token}")

    # Optional override: customize how users are created
    # async def create(
    #     self, user_create: UserCreate, safe: bool = False, request: Request | None = None
    # ) -> User:
    #     return await super().create(user_create, safe=safe, request=request)


# ✅ Dependency injection for the user manager (used internally by FastAPI Users)
async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    """
    Dependency to provide an instance of the custom UserManager.

    This is required by FastAPI Users to manage all user-related operations.

    Args:
        user_db: The user database adapter.

    Yields:
        UserManager: Instance of the custom manager.
    """
    yield UserManager(user_db)
