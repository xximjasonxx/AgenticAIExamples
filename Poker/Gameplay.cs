using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Orchestration.GroupChat;
using Microsoft.SemanticKernel.Agents.Runtime.InProcess;
using Microsoft.SemanticKernel.ChatCompletion;

namespace Farrellsoft.Examples.SemanticKernel.Poker
{
    public class Gameplay
    {
        private readonly ChatHistory _chatHistory = [];

        public required ChatCompletionAgent DealerAgent { get; init; }
        public List<ChatCompletionAgent> PlayerAgents { get; } = new List<ChatCompletionAgent>();

        public async Task PlayAsync(TimeSpan timeLength)
        {
            var allAgents = new List<ChatCompletionAgent> { DealerAgent };
            allAgents.AddRange(PlayerAgents);

            ValueTask responseCallback(ChatMessageContent response)
            {
                Console.WriteLine($"[{response.Role}] {response.Content}");
                _chatHistory.Add(response);
                return ValueTask.CompletedTask;
            }

#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
            var orchestration = new GroupChatOrchestration(
                new RoundRobinGroupChatManager() { MaximumInvocationCount = 100 },
                allAgents.ToArray()
            )
            { ResponseCallback = responseCallback };

            var runtime = new InProcessRuntime();
            await runtime.StartAsync();

            var result = await orchestration.InvokeAsync(
                $"Play a game of poker with {allAgents.Count} players. The dealer will deal cards and manage the game. Once the game is over terminate the orchestration",
                runtime
            );

            var output = await result.GetValueAsync(timeLength);
            Console.WriteLine($"\n# RESULT: {output}");
            Console.WriteLine("\n\nORCHESTRATION HISTORY");
            foreach (ChatMessageContent message in _chatHistory)
            {
                Console.WriteLine($"-- [{message.Role}] {message.Content}");
            }

            await runtime.StopAsync();
            _chatHistory.Clear();
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
        }
    }
}