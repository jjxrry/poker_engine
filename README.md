## Poker Hand Evaluator

by dotdev

## Project Abstract

---------------------------------------------------------------------------------------------------------------------------------


For this project, I plan to calculate the odds of achieving any given hand in Poker and beating the dealer, specifically Texas Hold 'em in a scenario of 2 players, the player and the dealer.

The project will rely on conditional probability through combinatorial mathematics and evaluate the winning percentage of the player's hand through an Effective Value (EV) formula at every stage of the game:

***Pre-Flop or Draw***

***Post-Flop***

***Fourth Card***

***River***


The evaluation will be run based on the possible acheivable hands in poker, namely:

***High Card***

***Pair***

***Two Pair***

***Three-of-a-Kind***

***Straight***

***Flush***

***Full House***

***Four-of-a-Kind***

***Straight Flush***

***Royal Flush***

---------------------------------------------------------------------------------------------------------------------------------

For each applicable stage of the game, the data will display the possibility of achieving any given hand through bar graph.

The y-axis will represent the different possible hands to achieve as mentioned above, while the x-axis will represent the probability of hitting any of the possible hands, calculated conditionally based on the draw of the dealer.

For the purposes of this project, we will assume that the system will calculate the win percentage based on what the system can see, we want extensibility for any outside party to view the game to see and be fed calculations knowing each opponent's hand as well. We want to approach calculating probability given a continuous addition of information about a sample size **n** by running calculations based on missing cards from the deck. 

To note, we are only calculating the possibility of achieving any given hand and comparing that to the possibilities of the dealer as well, for the scope of these simulations, we will not factor in "kickers" or the ability to evaluate the winning hand with the highest drawn card as a tiebreaker, given matching best hands. In evaluating possible hands, we will assign points to each card, with any successful hand to evaluate to a higher point value than any non-hand would achieve. We will then sum the EV of both the player and the dealer as event space and calculate the winning percentage of player, giving us:

$$ \text{Percentage of Winning} = \frac{Player EV}{Player EV + Dealer EV} $$


### **Initialization of Poker Game**

---------------------------------------------------------------------------------------------------------------------------------


To begin, we create class PokerGame to encapsulate game logic and maintain correctness for any alteration of the deck, resetting everytime we run a new game.

The functions for calculation will be defined at the top of this notebook and will be recalled for each instance, to simulate each stage within the game.

We have functions within the game that will be able to be called in a specific order, according to each stage of the game. When we run the logic, there is validation to ensure that we are in the right stage before executing any related code.

In the initial draw, we make sure that the player is dealt first, then the dealer.

We ensure that the turn and the river are not able to be dealt if the flop has not been dealt, and in the same vein, the flop is not able to be dealt unless there are no cards on the table.

It is also validated that the player and the dealer are not able to draw their initial 2 cards if they already have any cards drawn.

### **Case of Ace Low Straights**

---------------------------------------------------------------------------------------------------------------------------------

In the evaluation of hands, we are ranking 2-14 inclusively, but we need to catch the exception that Ace Low can still be considered a valid hand in a straight.

**Example:**

For the hand *[A, 2, 3, 4, 5]* we know that the Ace value by index is value 14, or 12 in a 0-12 scale. When we evaluate valid straights, we assume the assigned **A** is a high card, invalidating the hand as *[2, 3, 4, 5, A]*.

Now we need to catch that exception to validate the hand *[A, 2, 3, 4, 5]* with special cases for Ace-Low Straight in every hand that validates a Straight. (Straight, Straight Flush)


### **Calculation of probability to achieve any hand**

---------------------------------------------------------------------------------------------------------------------------------

In the instance of calculating the probability of hitting any hand, for the purposes of this simulation, we will factor in possible combinations of valid achievable hands given what the **system** sees as missing from the deck.

**For Example:**

We can know that the missing cards from the deck can factor into the ability to hit:

*If we draw 7 of Hearts, we know that the opponent cannot draw any hand that includes 7 of Hearts*.

### **Combinatorics of Evaluation Methods**

---------------------------------------------------------------------------------------------------------------------------------

For the purposes of the scope of the game, I believe it is prudent to document the current approach of combinatorial mathematics in the game engine and note improvments for the future to further align this engine with a larger scope.

Currently, we evaluate the hands combinatorially in the Post-Flop, and Post-Turn stages. We generate a hypothetical hand in the method that is used to evaluate the EV's that become summed and compared. We also use combinations to allow for extensibility when it comes to the scope, instead of evaluating just the next card, we can now adjust it to read for the next 2 unknown cards.

For the purposes of this, we simply iterate through the remaining deck.

It is clear that simply calculating the possibility of drawing a valid card to achieve a hand out the remaining deck is a simplification of true possibilities but there is much more work that does not seem plausible to achieve, given project timelines.

I am aware of the edge cases within this design.

***For Example:***

Currently, we do not evaluate the limited cards within a suit (for a flush) that must be calculated in the combinations rather than just the C(Remaining Deck, 1), we know that the more appropriate calculation must be more fleshed out to calculate how many of the same suit are remaining in the deck, then run the possibility of C(Remaining of Same Suit, 1). The reasoning behind this simplification is that to implement this effectively through all possible cases would be out of the scope of what is accomplishable given the current timeline.

### **Calculation of Winning Probabilities**

---------------------------------------------------------------------------------------------------------------------------------

For the instance of calculating winning probability, for ease of comparison and the lack of evaluating "kickers" in this simulation, we will follow a simple model of comparing the best possible hand that both players are able to create given the ***NEXT*** card that will be drawn on the table.

For Pre-Flop, we evaluate the EV of the 2-card hands

For Post-Flop, we calculate possible EV on the Turn

For Post-Turn, we calculate possible EV on the River

At Post-River, we calculate the EV based on all 7 cards available.


### **Plotting Data and Dynamic Updates**

---------------------------------------------------------------------------------------------------------------------------------

In the bottom section of the poker engine, there is implementation of a dynamically updated dictionary where we can update the running game based on the possibilities of hitting any given hand through simulating hand possibilites while factoring in the **next card**.

We update this bar graph by updating possibilities in the Post-Flop and Post-Turn stage, effectively analyzing any stage where there is an available **next card**.

There is no data for the Pre-Flop and Post-River as we are not considering the scope of three cards drawn at once, and we also do not need to factor in possible **next card** when all 7 cards are drawn in Post-River.


### **Concluding Thoughts**

---------------------------------------------------------------------------------------------------------------------------------

In writing this engine, there were many assumptions broken, methods revised, and scope adjustments that needed to be made to accomplish the end goal. 

I thought that even with simplifying heuristics and reducing hypothetical simulations, we could achieve something close to a truly comprehensive game engine. I quickly realized as the work piled up that the ability for a one person team to achieve something would have been out of scope given my other responsibilities. I want to thank Professor Veliz for his guidance and the overwhelming popularity of this same idea in StackOverflow and the Python community for having many discussions and documentation for how to achieve hand classification and deck initialization.

I will conclude this project here as I have outlined and achieved all my goals for the time being. 

I have accomplished:

-Python Poker Game Engine

-Calculation of EV based on probabilities drawn from the remaining deck and the valiation of all 10 poker hands

-Plotting data based on hypothetical **next hands** and using that data to inform a dynamically updating bar graph at each applicable game stage

There are many things that I would like to revisit, now reflecting on the project. I want to accurately calculate probabilty beyond a 52-card deck, similar to how real casinos would deal their cards. To implement this I would need to dynamically update and track remaining valid cards within the cards in the deck/pool, use this dynamically updating data to inform combinatoric calculations. 

There is also the idea of making the entire thing playable, with more opponents, action/betting cycles, but I digreess. Thank you very much for reading!