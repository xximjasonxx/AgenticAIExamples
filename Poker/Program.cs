
using Farrellsoft.Examples.SemanticKernel.Poker;
using Microsoft.SemanticKernel;
using Microsoft.Extensions.Configuration;

// Set up configuration
var configuration = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>()
    .Build();

var apiKey = configuration["AZURE_OPENAI_API_KEY"] 
    ?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY configuration value is required");

var endpoint = configuration["AZURE_OPENAI_ENDPOINT"] 
    ?? "https://openai-client-sandbox-eus2-mx01.openai.azure.com";

var dealerDeploymentName = configuration["DEALER_DEPLOYMENT_NAME"] 
    ?? "gpt-4o-mini-deployment";

var playerDeploymentName = configuration["PLAYER_DEPLOYMENT_NAME"] 
    ?? "o4-mini-deployment";

var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
    deploymentName: dealerDeploymentName,
    endpoint: endpoint,
    apiKey: apiKey,
    serviceId: "dealer"
);

builder.AddAzureOpenAIChatClient(
    deploymentName: playerDeploymentName,
    endpoint: endpoint,
    apiKey: apiKey,
    serviceId: "player"
);

var kernel = builder.Build();
var gameplay = new Gameplay
{
    DealerAgent = new DealerAgent(kernel).Agent
};

var numberOfPlayers = 6;
for (int index = 1; index <= numberOfPlayers; index++)
{
    gameplay.PlayerAgents.Add(new PlayerAgent(kernel, index, PlayMode.Normal).Agent);
};

await gameplay.PlayAsync(TimeSpan.FromMinutes(5));
Console.WriteLine("\nPress any key to exit...");
Console.ReadKey(true);