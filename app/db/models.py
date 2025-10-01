from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
from enum import Enum


class AssetType(str, Enum):
    """
    Enum for categorizing the type of financial asset.

    This helps in filtering, grouping, and analytics.
    """
    STOCK = "stock"
    ETF = "etf"
    CRYPTO = "crypto"
    OPTION = "option"
    MUTUAL_FUND = "mutual_fund"
    CASH = "cash"
    OTHER = "other"


class Holding(Base):
    """
    🧾 Represents a single asset held by a user in their portfolio.

    This model stores core information about the holding, such as:
    - Ticker and name
    - Quantity and purchase price
    - Asset type (e.g., stock, crypto)
    - Ownership (via user_id)

    Useful for displaying portfolio summaries, calculating gains/losses,
    and syncing with external APIs or dashboards.
    """

    __tablename__ = "holdings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        doc="Primary key: Unique identifier for this holding."
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        doc="Foreign key: Links this holding to the owning user."
    )

    symbol: Mapped[str] = mapped_column(
        String(length=10),
        nullable=False,
        index=True,
        doc="Ticker symbol (e.g., AAPL, BTC, VTI). Used for display and external API lookups."
    )

    name: Mapped[Optional[str]] = mapped_column(
        String(length=100),
        nullable=True,
        doc="Full name of the asset (e.g., Apple Inc.). Optional; can be enriched later."
    )

    quantity: Mapped[float] = mapped_column(
        nullable=False,
        doc="Number of units or shares held."
    )

    purchase_price: Mapped[float] = mapped_column(
        nullable=False,
        doc="Per-unit price paid at the time of purchase (in USD)."
    )

    purchase_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        doc="Date the asset was acquired. Defaults to now if not provided."
    )

    asset_type: Mapped[AssetType] = mapped_column(
        SQLEnum(AssetType),
        default=AssetType.STOCK,
        doc="Type of asset (e.g., stock, crypto, ETF). Useful for categorizing holdings."
    )

    notes: Mapped[Optional[str]] = mapped_column(
        String(length=255),
        nullable=True,
        doc="Optional user notes about the holding (e.g., investment strategy, goals)."
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        doc="Timestamp when the holding was created in the system."
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Timestamp of the most recent update to this holding."
    )
