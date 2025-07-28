import azure.functions as func
import json
from typing import Union, Tuple

from models import PriceHistoryRequest


def parse_request_body(req: func.HttpRequest) -> Tuple[Union[PriceHistoryRequest, None], Union[str, None]]:
    """
    Parse and deserialize HTTP request body to PriceHistoryRequest.
    
    Args:
        req: Azure Functions HTTP request object
        
    Returns:
        Tuple of (PriceHistoryRequest instance or None, error message or None)
    """
    try:
        # Get JSON body from request
        req_body = req.get_json()
        if not req_body:
            return None, "Request body is required. Expected JSON with 'ticketName' field."
        
        # Create model instance from JSON
        request_data = PriceHistoryRequest(**req_body)
        return request_data, None
        
    except TypeError as e:
        return None, f"Invalid request body structure: {str(e)}"
    except (ValueError, json.JSONDecodeError) as e:
        return None, "Invalid JSON in request body."
