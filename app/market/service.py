import yfinance as yf   
from typing import Dict

async def get_current_price(symbol: str) -> Dict[str, float]:
    """
    Fetch the latest market price for a ticker symbol using Yahoo finance.

    Args:
        symbol (str): Stock/ETF/crypto ticker symbol.

    Returns:
        dict: { "symbol": str, "current_price": float }
    """

    ticker = yf.Ticker(symbol)
    history = ticker.history(perioid="id")
    if history.empty:
        raise ValueError(f"No price data for {symbol}")

    price = history["Close"].iloc[-1]
    return {"symbol": symbol, "current_price": round(price, 2)}