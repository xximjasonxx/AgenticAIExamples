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
        "tickerName": "AAPL"
    }
    """
    logging.info('Python HTTP trigger function processed a request for stock price history.')
    
    # Parse and deserialize request body
    request_data = parse_request_body(req)
    if not request_data or request_data.tickerName.strip() == "":
        return func.HttpResponse(
            "Invalid request body. Expected JSON with 'tickerName'.",
            status_code=400
        )
    
    # figure out the range minus 1 month

    stock_service = StockService()

    
    user_id = req.headers.get('X-User-ID')
    timezone = req.headers.get('X-Timezone')
    local_time = req.headers.get('X-Local-Time')

    return func.HttpResponse(f"User ID: {user_id}, Timezone: {timezone}, Local Time: {local_time}")
