
import azure.functions as func
import logging
import json

from .request_parser import parse_request_body
from .date_service import DateService
from .stock_history_service import StockHistoryService

def register_get_price_history_function(app: func.FunctionApp):
    
    @app.route(route="get_price_history", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
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
        start_date, end_date = DateService.get_period()
        stock_service = StockHistoryService()
        price_data = stock_service.get_stock_history(
            ticker=request_data.tickerName.strip(),
            period_start=start_date,
            period_end=end_date)

        # Convert StockPriceData to list of dicts with date and price
        result = [{"date": stock.date, "price": stock.close} for stock in price_data]
        
        return func.HttpResponse(json.dumps(result), mimetype="application/json")