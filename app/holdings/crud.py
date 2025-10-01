from uuid import UUID
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Holding as holding_model
from app.holdings.schemas import HoldingCreate, HoldingUpdate


async def get_holding_by_id(
    db: AsyncSession, holding_id: int, user_id: UUID
) -> Optional[holding_model]:
    """
    Retrieve a specific holding by its ID and user.

    Args:
        db (AsyncSession): The database session.
        holding_id (int): The ID of the holding.
        user_id (UUID): The ID of the user (to enforce ownership).

    Returns:
        Optional[Holding]: The holding if found, else None.
    """
    result = await db.execute(
        select(holding_model).where(
            holding_model.id == holding_id,
            holding_model.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def get_all_holdings_for_user(
    db: AsyncSession, user_id: UUID
) -> List[holding_model]:
    """
    Retrieve all holdings owned by a specific user.

    Args:
        db (AsyncSession): The database session.
        user_id (UUID): The user's ID.

    Returns:
        List[Holding]: All holdings belonging to the user.
    """
    result = await db.execute(
        select(holding_model).where(holding_model.user_id == user_id)
    )
    return result.scalars().all()


async def create_holding(
    db: AsyncSession, holding_data: HoldingCreate, user_id: UUID
) -> holding_model:
    """
    Create a new holding for a user.

    Args:
        db (AsyncSession): The database session.
        holding_data (HoldingCreate): Input data for the new holding.
        user_id (UUID): The user ID to associate with the holding.

    Returns:
        Holding: The newly created holding object.
    """
    new_holding = holding_model(**holding_data.dict(), user_id=user_id)
    db.add(new_holding)
    await db.commit()
    await db.refresh(new_holding)
    return new_holding


async def update_holding(
    db: AsyncSession, holding_id: int, user_id: UUID, update_data: HoldingUpdate
) -> Optional[holding_model]:
    """
    Update an existing holding's fields.

    Args:
        db (AsyncSession): The database session.
        holding_id (int): The holding ID.
        user_id (UUID): The owner user ID.
        update_data (HoldingUpdate): Fields to update.

    Returns:
        Optional[Holding]: Updated holding if found and owned, else None.
    """
    result = await db.execute(
        select(holding_model).where(
            holding_model.id == holding_id,
            holding_model.user_id == user_id
        )
    )
    holding = result.scalar_one_or_none()
    if not holding:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(holding, field, value)

    await db.commit()
    await db.refresh(holding)
    return holding


async def delete_holding(
    db: AsyncSession, holding_id: int, user_id: UUID
) -> bool:
    """
    Delete a holding by ID (only if owned by the user).

    Args:
        db (AsyncSession): The database session.
        holding_id (int): The holding ID.
        user_id (UUID): The user ID.

    Returns:
        bool: True if deleted, False if not found or not owned.
    """
    result = await db.execute(
        select(holding_model).where(
            holding_model.id == holding_id,
            holding_model.user_id == user_id
        )
    )
    holding = result.scalar_one_or_none()
    if not holding:
        return False

    await db.delete(holding)
    await db.commit()
    return True
