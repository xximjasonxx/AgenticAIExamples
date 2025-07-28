import azure.functions as func
import datetime
import logging
import json

from models import PriceHistoryRequest

app = func.FunctionApp()

@app.route(route="get_price_history", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
def get_price_history(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get JSON body from request
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse(
                "Request body is required. Expected JSON with 'ticketName' field.",
                status_code=400
            )
        
        # Create model instance from JSON
        request_data = PriceHistoryRequest(**req_body)
        
        # Validate that ticketName is provided and not empty
        if not request_data.ticketName:
            return func.HttpResponse(
                "ticketName is required and cannot be empty.",
                status_code=400
            )
            
        return func.HttpResponse(f"Processing price history for ticket: {request_data.ticketName}")
        
    except TypeError as e:
        return func.HttpResponse(
            f"Invalid request body structure: {str(e)}",
            status_code=400
        )
    except (ValueError, json.JSONDecodeError) as e:
        return func.HttpResponse(
            "Invalid JSON in request body.",
            status_code=400
        )