from fastapi_users_db_sqlalchemy.generics import GUID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from uuid import uuid4, UUID
from app.db.database import Base

"""
SQLAlchemy model for the User table.

This defines the actual database structure for storing user accounts.
"""

class User(SQLAlchemyBaseUserTable[UUID], Base):  # ✅ Use UUID here
    __tablename__ = "users"

    # ✅ Add default=uuid4 to auto-generate UUIDs
    id: Mapped[UUID] = mapped_column(GUID, primary_key=True, default=uuid4)

    # Optional custom fields
    full_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
