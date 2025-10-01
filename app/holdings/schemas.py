from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import Optional


class AssetType(str, Enum):
    """
    Enumeration of possible asset types.
    Used to categorize a user's holding.
    """
    STOCK = "stock"
    ETF = "etf"
    CRYPTO = "crypto"
    OPTION = "option"
    MUTUAL_FUND = "mutual_fund"
    CASH = "cash"
    OTHER = "other"


class HoldingBase(BaseModel):
    """
    Shared base schema for holding-related models.
    Defines the common fields used in both creation and reading.
    """
    symbol: str = Field(..., description="Ticker or trading symbol (e.g., AAPL, BTC)")
    name: Optional[str] = Field(None, description="Human-readable asset name (optional)")
    quantity: float = Field(..., gt=0, description="Number of units or shares held")
    purchase_price: float = Field(..., gt=0, description="Price paid per unit at the time of purchase")
    purchase_date: Optional[datetime] = Field(
        None,
        description="Date and time of purchase (defaults to current time on server if omitted)"
    )
    asset_type: AssetType = Field(
        default=AssetType.STOCK,
        description="Classification of the asset (e.g., stock, crypto, ETF)"
    )
    notes: Optional[str] = Field(None, description="Free-form notes or tags for this holding")


class HoldingCreate(HoldingBase):
    """
    Schema for creating a new holding.
    Used in POST requests.
    """
    pass


class HoldingUpdate(BaseModel):
    """
    Schema for updating an existing holding.
    All fields are optional.
    """
    symbol: Optional[str] = Field(None, description="Updated ticker symbol")
    name: Optional[str] = Field(None, description="Updated asset name")
    quantity: Optional[float] = Field(None, gt=0, description="Updated number of units")
    purchase_price: Optional[float] = Field(None, gt=0, description="Updated price per unit")
    purchase_date: Optional[datetime] = Field(None, description="Updated purchase date")
    asset_type: Optional[AssetType] = Field(None, description="Updated asset type")
    notes: Optional[str] = Field(None, description="Updated notes")


class HoldingRead(HoldingBase):
    """
    Schema for reading a holding (e.g., in GET responses).
    Includes server-managed fields like ID and timestamps.
    """
    id: int = Field(..., description="Unique identifier for the holding")
    user_id: UUID = Field(..., description="UUID of the user who owns this holding")
    created_at: datetime = Field(..., description="Timestamp when the holding was created")
    updated_at: datetime = Field(..., description="Timestamp when the holding was last updated")

    class Config:
        orm_mode = True  # ✅ Allows Pydantic to work seamlessly with SQLAlchemy models
