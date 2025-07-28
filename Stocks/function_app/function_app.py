import azure.functions as func
import datetime
import logging
import json
import asyncio
from dataclasses import asdict

from request_parser import parse_request_body
from stock_service import StockService

app = func.FunctionApp()

@app.route(route="get_price_history", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
def get_price_history(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to get stock price history.
    Uses dependency injection to access the stock service.
    
    Expected request body:
    {
        "tickerName": "AAPL",
        "period": "1y"  // optional, defaults to "1y"
    }
    """
    logging.info('Python HTTP trigger function processed a request for stock price history.')
    
    # Parse and deserialize request body
    request_data = parse_request_body(req)

    return func.HttpResponse(None, status_code=200)