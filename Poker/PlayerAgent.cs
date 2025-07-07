using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;

namespace Farrellsoft.Examples.SemanticKernel.Poker
{
    public class PlayerAgent
    {
        public ChatCompletionAgent Agent { get;  private set; }

        public PlayerAgent(Kernel kernel, int playerNumber, PlayMode playMode)
        {
            Agent = new ChatCompletionAgent()
            {
                Kernel = kernel,
                Name = $"Player{playerNumber}",
                Description = $"A player in the poker game called Player {playerNumber}. You receive cards and make decisions based on your hand.",
                Instructions = """
                You are a player in a poker game. Your role is to:
                1) Receive two cards from the dealer.
                2) Decide whether to place a bet, check, or fold based on your hand.
                3) Participate in the game by responding to the dealer's prompts.

                You do not announce your actions to the other players, only to the dealer who will then notify the table.
                """,
            };
        }
    }
}