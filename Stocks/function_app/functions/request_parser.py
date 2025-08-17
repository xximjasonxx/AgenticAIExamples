import azure.functions as func

from shared.models import PriceHistoryRequest

def parse_request_body(req: func.HttpRequest) -> PriceHistoryRequest:
    """
    Parse and deserialize HTTP request body to PriceHistoryRequest.
    
    Args:
        req: Azure Functions HTTP request object
        
    Returns:
        Tuple of (PriceHistoryRequest instance or None, error message or None)
    """
    
    # Get JSON body from request
    req_body = req.get_json()
    ticker_name = req_body.get('tickerName', '').strip()
    
    return PriceHistoryRequest(
        tickerName=ticker_name
    )
