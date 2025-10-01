from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.database import get_async_session
from app.users.models import User
from app.users.deps import current_active_user

from app.holdings import crud
from app.holdings.schemas import HoldingCreate, HoldingRead, HoldingUpdate

router = APIRouter(
    prefix="/holdings",
    tags=["holdings"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[HoldingRead])
async def get_user_holdings(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    ✅ Get all holdings for the currently authenticated user.
    """
    return await crud.get_all_holdings_for_user(db, user.id)


@router.get("/{holding_id}", response_model=HoldingRead)
async def get_holding_by_id(
    holding_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    ✅ Retrieve a specific holding by ID.
    Only returns if the holding belongs to the current user.
    """
    holding = await crud.get_holding_by_id(db, holding_id, user.id)
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found.")
    return holding


@router.post("/", response_model=HoldingRead, status_code=status.HTTP_201_CREATED)
async def create_holding(
    holding_in: HoldingCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    ✅ Create a new holding for the current user.
    """
    return await crud.create_holding(db, holding_in, user.id)


@router.put("/{holding_id}", response_model=HoldingRead)
async def update_holding(
    holding_id: int,
    holding_update: HoldingUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    ✅ Update an existing holding.
    Only allowed if the holding belongs to the current user.
    """
    updated = await crud.update_holding(db, holding_id, user.id, holding_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Holding not found or not authorized.")
    return updated


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holding(
    holding_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    ✅ Delete a holding by ID.
    Only allowed if the holding belongs to the current user.
    """
    success = await crud.delete_holding(db, holding_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Holding not found or not authorized.")
    return None
