import azure.functions as func
import datetime
import logging

from request_parser import parse_request_body

app = func.FunctionApp()

@app.route(route="get_price_history", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
def get_price_history(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Parse and deserialize request body
    request_data, error = parse_request_body(req)
    if error:
        return func.HttpResponse(error, status_code=400)
    
    # Validate that tickerName is provided and not empty
    if not request_data.tickerName:
        return func.HttpResponse(
            "tickerName is required and cannot be empty.",
            status_code=400
        )

    return func.HttpResponse(f"Processing price history for ticker: {request_data.tickerName}")