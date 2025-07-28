# Stock Price History Azure Function

This Azure Function app provides a REST API for fetching stock price history using dependency injection and secure configuration management.

## Architecture

The application implements several key patterns:

- **Dependency Injection**: Services are managed through a DI container
- **Service Abstraction**: Interface-based design allows for easy testing and mocking
- **Secure Configuration**: API keys are loaded from environment variables or local settings
- **Error Handling**: Comprehensive error handling with retry logic
- **Async Operations**: Full async/await support for external API calls

## Project Structure

```
function_app/
├── function_app.py              # Main Azure Function entry point
├── stock_service.py             # Stock data service implementation
├── dependency_injection.py     # DI container and service registration
├── models.py                   # Data models and DTOs
├── request_parser.py           # HTTP request parsing logic
├── test_stock_service.py       # Test script for service validation
├── requirements.txt            # Python dependencies
├── local.settings.json         # Local development configuration
└── host.json                   # Azure Functions host configuration
```

## Configuration

### Environment Variables

- `EodhdStocksApiKey`: API key for EOD Historical Data service
- `USE_MOCK_SERVICES`: Set to "true" to use mock services instead of real API calls

### Local Development

For local development, add your API key to `local.settings.json`:

```json
{
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "EodhdStocksApiKey": "your-api-key-here",
    "USE_MOCK_SERVICES": "false"
  }
}
```

### Production Deployment

For production, set the environment variables in your Azure Function App settings:

- Navigate to your Function App in Azure Portal
- Go to Configuration → Application Settings
- Add `EodhdStocksApiKey` with your API key value

## API Usage

### Endpoint

```
POST /api/get_price_history
```

### Request Format

```json
{
  "tickerName": "AAPL",
  "period": "1y"
}
```

### Parameters

- `tickerName` (required): Stock ticker symbol (e.g., "AAPL", "MSFT", "GOOGL")
- `period` (optional): Time period for historical data. Defaults to "1y"
  - Supported values: "1d", "5d", "1m", "3m", "6m", "1y", "2y", "5y", "10y"

### Response Format

#### Success Response (200)

```json
{
  "ticker": "AAPL",
  "success": true,
  "total_records": 252,
  "error_message": null,
  "data": [
    {
      "date": "2024-01-01",
      "open": 150.0,
      "high": 155.0,
      "low": 148.0,
      "close": 152.0,
      "volume": 1000000,
      "adjusted_close": 152.0
    }
  ]
}
```

#### Error Response (400/500)

```json
{
  "ticker": "INVALID",
  "success": false,
  "total_records": 0,
  "error_message": "Ticker 'INVALID' not found",
  "data": []
}
```

## Service Architecture

### Stock Service

The `StockService` class implements the `IStockService` interface and provides:

- **Secure API Key Management**: Loads keys from environment variables or local settings
- **Retry Logic**: Exponential backoff for handling transient failures
- **Error Handling**: Comprehensive error handling for various API failure scenarios
- **Resource Management**: Proper HTTP session management and cleanup

### Dependency Injection

The DI container (`ServiceContainer`) provides:

- **Singleton Services**: One instance per container lifetime
- **Transient Services**: New instance on each request
- **Environment-Based Registration**: Automatic mock/real service selection
- **Resource Cleanup**: Automatic cleanup of services that support it

### Mock Services

For testing and development, mock services are available:

- **MockStockService**: Returns sample data without external API calls
- **Controlled Testing**: Enables testing without API quotas or network dependencies

## Development

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your API key in `local.settings.json`

3. Start the function app:
   ```bash
   func start
   ```

### Testing

Run the test script to validate service functionality:

```bash
python test_stock_service.py
```

### Using Mock Services

Set `USE_MOCK_SERVICES=true` in your environment to use mock data:

```json
{
  "Values": {
    "USE_MOCK_SERVICES": "true"
  }
}
```

## Security Considerations

- **No Hardcoded Credentials**: API keys are loaded from secure configuration
- **Environment Separation**: Different configurations for development and production
- **Secure Transport**: All external API calls use HTTPS
- **Input Validation**: Comprehensive validation of all inputs
- **Error Information**: Sensitive information is not exposed in error messages

## Error Handling

The service implements comprehensive error handling:

- **Validation Errors**: Invalid or missing parameters
- **Authentication Errors**: Invalid API keys
- **Network Errors**: Connection failures with retry logic
- **API Errors**: Service-specific error responses
- **Timeout Handling**: Configurable timeouts for all operations

## Logging

All operations are logged with appropriate levels:

- **Info**: Successful operations and general flow
- **Warning**: Recoverable errors and validation issues
- **Error**: Service failures and unexpected errors

## Performance Considerations

- **Connection Pooling**: Reused HTTP connections for efficiency
- **Async Operations**: Non-blocking operations throughout
- **Resource Management**: Proper cleanup and resource disposal
- **Caching Ready**: Service design supports future caching implementation

## Extending the Service

To add new stock data providers:

1. Implement the `IStockService` interface
2. Register the new service in `ServiceFactory.create_container()`
3. Add any new configuration requirements

To add new endpoints:

1. Create new models in `models.py`
2. Add request parsing logic
3. Implement the function in `function_app.py`
4. Register any new services in the DI container
