
from dataclasses import dataclass
from typing import Optional

@dataclass
class PriceHistoryRequest:
    tickerName: str

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