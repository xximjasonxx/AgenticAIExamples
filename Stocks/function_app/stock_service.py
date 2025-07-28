from datetime import datetime
from models import StockPriceData
from typing import  List

class StockService:
  def __init__(self, api_key: str):
    self.api_key = api_key

  def get_stock_history(self, ticker: str, period_start: datetime, period_end: datetime) -> List[StockPriceData]:
    """
    Fetch stock price history for a given ticker within the specified period.
    
    Args:
        ticker: Stock ticker symbol
        period_start: Start date of the period
        period_end: End date of the period
        
    Returns:
        PriceHistoryResponse containing stock data or error information
    """
    return []