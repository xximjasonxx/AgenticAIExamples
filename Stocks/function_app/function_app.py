import azure.functions as func
from functions import (
  register_get_price_history_function,
register_get_company_info_function
)

app = func.FunctionApp()
register_get_price_history_function(app)
register_get_company_info_function(app)