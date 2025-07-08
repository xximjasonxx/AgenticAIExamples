
using Farrellsoft.Examples.SemanticKernel.Poker;
using Microsoft.SemanticKernel;
using Microsoft.Extensions.Configuration;
using OpenAI;

// Set up configuration
var configuration = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>()
    .Build();

var apiKey = configuration["AZURE_OPENAI_API_KEY"] 
    ?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY configuration value is required");
var endpoint = "https://openai-client-sandbox-eus2-mx01.openai.azure.com";

var builder = Kernel.CreateBuilder();

builder.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4o-mini-deployment",
    endpoint: endpoint,
    apiKey: apiKey,
    serviceId: "dealer"
);

builder.AddAzureOpenAIChatClient(
    deploymentName: "o4-mini-deployment",
    endpoint: endpoint,
    apiKey: apiKey,
    serviceId: "player"
);

var kernel = builder.Build();
var gameplay = new Game
{
    DealerAgent = new DealerAgent(kernel).Agent
};

var numberOfPlayers = 6;
for (int index = 1; index <= numberOfPlayers; index++)
{
    gameplay.PlayerAgents.Add(new PlayerAgent(kernel, index, PlayMode.Normal).Agent);
};

try
{
    await gameplay.PlayAsync(TimeSpan.FromMinutes(5));
}
catch (AggregateException aex)
{
    foreach (var inner in aex.InnerExceptions)
    {
        Console.WriteLine($"An aggregated error occurred: {inner.Message}");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"An error occurred: {ex.Message}");
}
Console.WriteLine("\nPress any key to exit...");
Console.ReadKey(true);