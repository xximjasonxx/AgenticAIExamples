using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Magentic;
using Microsoft.SemanticKernel.Agents.Orchestration.GroupChat;
using Microsoft.SemanticKernel.Agents.Runtime.InProcess;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;

#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0001 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0101 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

namespace Farrellsoft.Examples.SemanticKernel.Poker
{
    public class Game
    {
        private readonly ChatHistory _chatHistory = [];

        public required ChatCompletionAgent DealerAgent { get; init; }
        public List<ChatCompletionAgent> PlayerAgents { get; } = new List<ChatCompletionAgent>();

        public async Task PlayAsync(Kernel kernel, TimeSpan timeLength)
        {
            ValueTask responseCallback(ChatMessageContent response)
            {
                Console.WriteLine($"[{response.AuthorName}] {response.Content}");
                _chatHistory.Add(response);
                Console.WriteLine();

                return ValueTask.CompletedTask;
            }

            // create the magenetic manager
            var manager = new StandardMagenticManager(
                kernel.GetRequiredService<IChatCompletionService>(serviceKey: "dealer"),
                new AzureOpenAIPromptExecutionSettings()
                {
                    Temperature = 0.2f
                });

            _chatHistory.Clear();

            // Combine dealer agent and player agents
            var allAgents = new List<ChatCompletionAgent> { DealerAgent };
            allAgents.AddRange(PlayerAgents);

            // create the orchestrator
            var orchestrator = new MagenticOrchestration(manager, allAgents.ToArray())
            {
                ResponseCallback = responseCallback,
                LoggerFactory = kernel.LoggerFactory,
            };

            var runtime = new InProcessRuntime();
            await runtime.StartAsync();

            var prompt = $"""
                You are to play a single game of Texas Hold'em Poker using standard rules with {PlayerAgents.Count} players.
                Between each action, provide a summary of the current game state
                Once the hand is complete, announce the winner and end the game.
            """;

            var gameResult = await orchestrator.InvokeAsync(prompt, runtime);
            var textResult = await gameResult.GetValueAsync(timeLength);
            Console.WriteLine(textResult);

            await runtime.RunUntilIdleAsync();
        }
    }
}

#pragma warning restore SKEXP0001 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning restore SKEXP0101 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.