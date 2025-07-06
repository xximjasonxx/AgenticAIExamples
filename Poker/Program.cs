
using Farrellsoft.Examples.SemanticKernel.Poker;

var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4o-mini-deployment",
    endpoint: "https://openai-client-sandbox-eus2-mx01.openai.azure.com",
    apiKey: builder.Configuration["AZURE_OPENAI_API_KEY"],
    serviceId: "dealer"
);

builder.AddAzureOpenAIChatClient(
    deploymentName: "o4-mini-deployment",
    endpoint: "https://openai-client-sandbox-eus2-mx01.openai.azure.com",
    apiKey: builder.Configuration["AZURE_OPENAI_API_KEY"],
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