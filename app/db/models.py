from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Holdings(Base):
    """
    Database model for portfolio holdings.
    Each holding is linked to a specific user via user_id.
    """
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    amount = Column(Float)
    avg_buy_price = Column(Float)

    # 🔐 FK to the users table (UUID is default for fastapi-users)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Optional reverse relationship
    # user = relationship("User", back_populates="holdings")


