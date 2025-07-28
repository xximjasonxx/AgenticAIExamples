from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PriceHistoryRequest:
    tickerName: str
    period: Optional[str] = "1y"  # Default to 1 year

@dataclass
class StockPriceData:
    """Data model for individual stock price data point."""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None
