using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using System.Net;
using System.Text.Json;
using api.Services;

namespace api
{
    public class SendQueryFunction
    {
        private readonly ILogger _logger;

        public SendQueryFunction(ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger<SendQueryFunction>();
        }

        [Function("send_query")]
        public async Task<HttpResponseData> Run(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "send")] HttpRequestData req)
        {
            _logger.LogInformation("Processing send_query request");

            try
            {
                // Read the request body
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                
                if (string.IsNullOrEmpty(requestBody))
                {
                    var badRequestResponse = req.CreateResponse(HttpStatusCode.BadRequest);
                    await badRequestResponse.WriteStringAsync("Request body cannot be empty");
                    return badRequestResponse;
                }

                // Parse JSON and validate the query field
                JsonDocument jsonDoc;
                try
                {
                    jsonDoc = JsonDocument.Parse(requestBody);
                }
                catch (JsonException)
                {
                    var badRequestResponse = req.CreateResponse(HttpStatusCode.BadRequest);
                    await badRequestResponse.WriteStringAsync("Invalid JSON format");
                    return badRequestResponse;
                }

                // Check if the query field exists
                if (!jsonDoc.RootElement.TryGetProperty("query", out JsonElement queryElement))
                {
                    var badRequestResponse = req.CreateResponse(HttpStatusCode.BadRequest);
                    await badRequestResponse.WriteStringAsync("Missing 'query' field in request body");
                    return badRequestResponse;
                }

                string query = queryElement.GetString() ?? "";

                // Call the injected SearchService to get the response
                string result = string.Empty;  //await _searchService.GetResponse(query);

                var response = req.CreateResponse(HttpStatusCode.OK);
                await response.WriteStringAsync(result);
                return response;
                
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing send_query request");
                var errorResponse = req.CreateResponse(HttpStatusCode.InternalServerError);
                await errorResponse.WriteStringAsync("Internal server error");
                return errorResponse;
            }
        }
    }
}
