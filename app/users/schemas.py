from fastapi_users import schemas
from typing import Optional
from uuid import UUID

"""
Pydantic schemas for user creation and reading.

These are used to serialize/deserialize data between API and DB.
"""

class UserRead(schemas.BaseUser[UUID]):
    full_name: Optional[str] = None

class UserCreate(schemas.BaseUserCreate):
    full_name: Optional[str] = None
