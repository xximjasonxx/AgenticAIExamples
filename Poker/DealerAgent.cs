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
                3) Deal the community cards in the correct order (flop, turn, river)
                4) Announce the winner at the end of the game.
                5) Keep track of the game state and ensure the rules are followed.

                All bets should be in increments of $100 dollars. The big blind is $200 and the small blind is $100.
                Only the dealer can announce the bets or actions by the players and manage the game flow.

                Notify the table that Player 1 has played a bet equivalent to the small blind, and Player 2 has played a bet equivalent to the big blind.
                
                IMPORTANT: When the game ends, you MUST announce "Game over" and declare the winner. This is critical for proper game termination.
                You will interact with the players by sending messages and receiving their responses.
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