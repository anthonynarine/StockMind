from pydantic import BaseModel, Field

class HoldingCreate(BaseModel):
    ticker: str = Field(..., description="Asset symbol (e.g., BTC, NVDA, ETH")
    amount: float = Field(..., gt=0, description="Number of shares or coins owned")
    avg_buy_price: float = Field(..., gt=0, description="Average purchase price")