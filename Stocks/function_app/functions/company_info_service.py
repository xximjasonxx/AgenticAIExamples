import os
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from typing import List

class CompanyInfoService:
  def __init__(self) -> None:
    pass

  def get_company_info(self, ticker: str) -> dict:
    """
    Get comprehensive company information including basic info and dividends.
    Executes both _get_information and _get_dividends in parallel for efficiency.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary containing combined company information and dividend data
    """
    ticker_upper = ticker.upper()
    
    # Execute both API calls in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:
      # Submit both tasks
      info_future = executor.submit(self._get_information, ticker_upper)
      dividends_future = executor.submit(self._get_dividends, ticker_upper)
      
      # Get results from both futures
      company_info = info_future.result()
      dividends = dividends_future.result()
    
    # Combine the results into a single dictionary
    combined_result = {
      **company_info,  # Spread company info fields
      "dividends": dividends  # Add dividends as a separate field
    }
    
    return combined_result
  
  def _get_dividends(self, ticker: str) -> List[dict]:
    """
    Fetch dividend information for a given ticker from Polygon.io.

    Args:
        ticker: Stock ticker symbol

    Returns:
        List of dictionaries containing dividend information or empty list on error
        Each dictionary contains the keys: cashAmount, pay_date, declaration_date
    """
    # Read configuration from environment
    base_url = os.getenv("PolygonBaseUrl")
    api_key = os.getenv("PolygonApiKey")

    if not base_url or not api_key:
      # Missing configuration
      return []

    # Calculate 6 months ago from today
    six_months_ago = datetime.now() - timedelta(days=180)

    # Ensure ticker is safe for URLs
    ticker_safe = urllib.parse.quote(ticker.strip())
    api_key_safe = urllib.parse.quote(api_key)

    # Build the request URL for dividends
    url = f"{base_url.rstrip('/')}/v3/reference/dividends?ticker={ticker_safe}&order=desc&limit=50&sort=ex_dividend_date&apiKey={api_key_safe}"

    try:
      with urllib.request.urlopen(url, timeout=10) as resp:
        if getattr(resp, 'status', None) not in (None, 200) and resp.status != 200:
          return []

        raw = resp.read().decode()
        data = json.loads(raw) if raw else {}
        results = data.get("results") or []

        # Filter dividends from the last 6 months and extract required fields
        filtered_dividends = []
        for dividend in results:
          ex_dividend_date_str = dividend.get("ex_dividend_date")
          if not ex_dividend_date_str:
            continue
          
          # Parse the ex_dividend_date
          try:
            ex_dividend_date = datetime.strptime(ex_dividend_date_str, '%Y-%m-%d')
            # Only include dividends from the last 6 months
            if ex_dividend_date >= six_months_ago:
              filtered_dividends.append({
                "cashAmount": dividend.get("cash_amount"),
                "payDate": dividend.get("pay_date"),
                "declarationDate": dividend.get("declaration_date")
              })
          except ValueError:
            # Skip dividends with invalid date format
            continue

        return filtered_dividends
    except Exception:
      # Any error (network, JSON, etc.) results in empty response
      return []

  def _get_information(self, ticker: str) -> dict:
    """
    Fetch company information for a given ticker from Polygon.io.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary containing the requested company information or empty dict on error
        The returned dict contains the keys: description, name, totalEmployees, listDate
    """
    # Read configuration from environment
    base_url = os.getenv("PolygonBaseUrl")
    api_key = os.getenv("PolygonApiKey")

    if not base_url or not api_key:
      # Missing configuration
      return {}

    # Ensure ticker is safe for URLs
    ticker_safe = urllib.parse.quote(ticker.strip())

    # Build the request URL
    url = f"{base_url.rstrip('/')}/v3/reference/tickers/{ticker_safe}?apiKey={urllib.parse.quote(api_key)}"

    try:
      with urllib.request.urlopen(url, timeout=10) as resp:
        # urllib responses expose .status in modern Python
        if getattr(resp, 'status', None) not in (None, 200) and resp.status != 200:
          return {}

        raw = resp.read().decode()
        data = json.loads(raw) if raw else {}
        results = data.get("results") or {}

        return {
          "description": results.get("description"),
          "name": results.get("name"),
          "totalEmployees": results.get("total_employees"),
          "listDate": results.get("list_date"),
          "marketCap": results.get("market_cap")
        }
    except Exception:
      # Any error (network, JSON, etc.) results in empty response
      return {}