import azure.functions as func
import json
from typing import Callable
from functools import wraps

def json_body(model_class):
    """Decorator to automatically deserialize JSON body to a dataclass"""
    def decorator(func_handler: Callable) -> Callable:
        @wraps(func_handler)
        def wrapper(req: func.HttpRequest) -> func.HttpResponse:
            try:
                req_body = req.get_json()
                if not req_body:
                    return func.HttpResponse(
                        f"Request body is required. Expected JSON matching {model_class.__name__}.",
                        status_code=400
                    )
                
                # Create model instance from JSON
                model_instance = model_class(**req_body)
                
                # Call the original function with the deserialized model
                return func_handler(model_instance)
                
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
        return wrapper
    return decorator
