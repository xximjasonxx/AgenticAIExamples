import azure.functions as func
from functions import register_get_price_history_function

app = func.FunctionApp()
register_get_price_history_function(app)