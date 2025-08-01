from datetime import datetime
from models import StockPriceData
from typing import List
import os
import aiohttp
import asyncio

class StockService:
  def __init__(self):
    pass

  def get_stock_history(self, ticker: str, period_start: datetime, period_end: datetime) -> List[StockPriceData]:
    """
    Fetch stock price history for a given ticker within the specified period.
    
    Args:
        ticker: Stock ticker symbol
        period_start: Start date of the period
        period_end: End date of the period
        
    Returns:
        List[StockPriceData] containing stock data or empty list on error
    """
    # Get API token from environment variable
    api_token = os.getenv('EodhdStocksApiKey')
    if not api_token:
        raise ValueError("EodhdStocksApiKey environment variable is not set")
    
    # Format dates as YYYY-MM-dd
    from_date = period_start.strftime('%Y-%m-%d')
    to_date = period_end.strftime('%Y-%m-%d')
    
    # Construct the API URL
    url = f"https://eodhd.com/api/eod/{ticker.lower()}?from={from_date}&to={to_date}&period=d&api_token={api_token}&fmt=json"
    
    try:
        # Use asyncio to run the async HTTP request
        return asyncio.run(self._fetch_stock_data_async(url))
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return []
  
  async def _fetch_stock_data_async(self, url: str) -> List[StockPriceData]:
    """
    Async helper method to fetch stock data from the API.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Convert API response to StockPriceData objects
                stock_data = []
                for item in data:
                    # Map API response to StockPriceData model
                    stock_price = StockPriceData(
                        date=item.get('date'),
                        open=float(item.get('open', 0)),
                        high=float(item.get('high', 0)),
                        low=float(item.get('low', 0)),
                        close=float(item.get('close', 0)),
                        volume=int(item.get('volume', 0)),
                        adjusted_close=float(item.get('adjusted_close')) if item.get('adjusted_close') else None
                    )
                    stock_data.append(stock_price)
                return stock_data
            else:
                print(f"API request failed with status {response.status}")
                return []