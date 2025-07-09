using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Connectors.OpenAI;

namespace Farrellsoft.Examples.SemanticKernel.Poker
{
    public class DealerAgent
    {
        public ChatCompletionAgent Agent { get; private set; }

        public DealerAgent(Kernel kernel)
        {
            Agent = new ChatCompletionAgent()
            {
                Kernel = kernel,
                Name = "Dealer",
                Description = "The dealer in a poker game. You deal cards to the players and facilitate the game.",
                Instructions = """
                You are the dealer in a poker game. Perform the following tasks:
                1) Deal two cards to each player, one at a time. Identify the cards dealt to each player.
                2) Announce the start of the game and ask for players to place their bets, check, or fold
                    - In Pre-flop betting:
                        - The first player to act is the player to the left of the big blind.
                        - The small blind acts first, followed by the big blind.
                        - The big blind is the last to bet in pre-flop betting.
                    - In post-flop betting:
                        - The first player to act is the player to the left of the dealer.
                3) Deal the community cards in the correct order (flop, turn, river)
                4) Announce the winner at the end of the game.

                Ensure all bets are in increments of $100 dollars. The big blind is $200 and the small blind is $100.
                The total amount given to each player is $1000.
                """,
                Arguments = new KernelArguments(new OpenAIPromptExecutionSettings()
                {
                    Temperature = 0.2f,
                    ServiceId = "dealer"
                })
            };
        }
    }
}