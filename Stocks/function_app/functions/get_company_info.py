
import azure.functions as func
import logging
import json

from .request_parser import parse_request_body
from .company_info_service import CompanyInfoService

def register_get_company_info_function(app: func.FunctionApp):
  @app.route(route="get_company_info", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
  def get_company_info(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing get_company_info request")
    request_data = parse_request_body(req)
    if not request_data or request_data.tickerName.strip() == "":
        return func.HttpResponse(
            "Invalid request body. Expected JSON with 'tickerName'.",
            status_code=400
        )

    service = CompanyInfoService()
    company_info = service.get_company_info(request_data.tickerName.strip())
    if not company_info:
        return func.HttpResponse("Company information not found", status_code=404)

    return func.HttpResponse(json.dumps(company_info), mimetype="application/json")