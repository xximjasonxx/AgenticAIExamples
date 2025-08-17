
import azure.functions as func
import logging
import json

from .request_parser import parse_request_body

def register_get_company_info_function(app: func.FunctionApp):

  @app.route(route="get_company_info", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
  def get_company_info(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Not implemented", status_code=501)