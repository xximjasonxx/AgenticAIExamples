using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Orchestration.GroupChat;
using Microsoft.SemanticKernel.Agents.Runtime.InProcess;
using Microsoft.SemanticKernel.ChatCompletion;

#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning disable SKEXP0001 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

namespace Farrellsoft.Examples.SemanticKernel.Poker
{
    public class Game
    {
        private readonly ChatHistory _chatHistory = [];
        private bool _gameOver = false;

        public required ChatCompletionAgent DealerAgent { get; init; }
        public List<ChatCompletionAgent> PlayerAgents { get; } = new List<ChatCompletionAgent>();

        public async Task PlayAsync(TimeSpan timeLength)
        {
            // Create agent list with dealer interleaved after each player
            var allAgents = new List<ChatCompletionAgent>();
            
            // Start with dealer to set up the game
            allAgents.Add(DealerAgent);
            
            // Add each player followed by dealer for evaluation
            foreach (var player in PlayerAgents)
            {
                allAgents.Add(player);
                allAgents.Add(DealerAgent); // Dealer evaluates after each player
            }

            using var cancellationTokenSource = new CancellationTokenSource(timeLength);

            ValueTask responseCallback(ChatMessageContent response)
            {
                Console.WriteLine($"[{response.AuthorName}] {response.Content}");
                _chatHistory.Add(response);

                // Check if dealer announced game over
                if (response.AuthorName == "Dealer" &&
                    (response.Content?.Contains("Game over", StringComparison.OrdinalIgnoreCase) == true ||
                     response.Content?.Contains("game is over", StringComparison.OrdinalIgnoreCase) == true ||
                     response.Content?.Contains("winner", StringComparison.OrdinalIgnoreCase) == true))
                {
                    Console.WriteLine("\n*** GAME OVER DETECTED - TERMINATING GAME ***");
                    _gameOver = true;
                    cancellationTokenSource.Cancel();
                    return ValueTask.CompletedTask;
                }

                // Prompt human for input between agent calls
                Console.WriteLine("\n--- Press any key to continue to the next agent action ---");
                Console.ReadKey(true);
                Console.WriteLine();

                return ValueTask.CompletedTask;
            }

            var orchestration = new GroupChatOrchestration(
                new RoundRobinGroupChatManager() { MaximumInvocationCount = 100 },
                allAgents.ToArray()
            )
            { ResponseCallback = responseCallback };

            var runtime = new InProcessRuntime();
            await runtime.StartAsync();

            try
            {
                var result = await orchestration.InvokeAsync(
                    $"Play a game of poker with {PlayerAgents.Count} players. The dealer will deal cards and manage the game. Once the game is over, announce 'Game over' and the winner.",
                    runtime
                );

                if (!_gameOver)
                {
                    await result.GetValueAsync(timeLength);
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("\nGame terminated successfully.");
            }

            await runtime.StopAsync();
            _chatHistory.Clear();
        }
    }
}

#pragma warning restore SKEXP0001 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.