import azure.functions as func
import datetime
import logging

from models import PriceHistoryRequest
from decorators import json_body

app = func.FunctionApp()

@app.route(route="get_price_history", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
@json_body(PriceHistoryRequest)
def get_price_history(request: PriceHistoryRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Validate that ticketName is provided and not empty
    if not request.ticketName:
        return func.HttpResponse(
            "ticketName is required and cannot be empty.",
            status_code=400
        )
        
    return func.HttpResponse(f"Processing price history for ticket: {request.ticketName}")