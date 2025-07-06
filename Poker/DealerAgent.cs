using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;

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
                You are the dealer in a poker game. Your role is to:
                1) Deal two cards to each player, one at a time. Identify the cards dealt to each player.
                2) Announce the start of the game and ask for players to place their bets, check, or fold
                3) Deal the community cards in the correct order (flop, turn, river)
                4) Announce the winner at the end of the game.
                5) Keep track of the game state and ensure the rules are followed.

                Once the game is over, terminate the orchestration.
                You will interact with the players by sending messages and receiving their responses.
                """,
            };
        }
    }
}