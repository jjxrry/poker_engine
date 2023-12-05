import matplotlib.pyplot as plt
import random
import math
from collections import Counter
from collections import defaultdict
from itertools import combinations

class PokerGame:
    def __init__(self):
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['H', 'D', 'C', 'S']
        self.deck = [(v, s) for v in self.values for s in self.suits]
        self.drawn_player = []
        self.drawn_dealer = []
        self.cards_on_table = []
        self.hand_data = {'High': 0, 'Pair': 0, '2Pair': 0, '3Kind': 0, 
                          'Str': 0, 'Flush': 0, 'FH': 0, '4Kind': 0, 
                          'SF': 0, 'RF': 0}

    def combination(self, n, k):
        return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

    def shuffle(self):
        random.shuffle(self.deck)

    def initial_draw_player(self):
        if len(self.drawn_player) == 0:
            for i in range(2):
                self.drawn_player.append(self.deck.pop())

    def initial_draw_dealer(self):
        if len(self.drawn_dealer) == 0:
            for i in range(2):
                self.drawn_dealer.append(self.deck.pop())

    def draw_initial_hands(self):
        self.initial_draw_player()
        self.initial_draw_dealer()
        self.calculate_preflop_percentage(self.drawn_player, self.drawn_dealer)

    def calculate_preflop_strength(self, hand):
        if self.has_pair(hand):
            return 3
        # Suited
        elif hand[0][1] == hand[1][1]:
            return 2
        # Assume high card value as lowest strength
        else:
            return 1

    def calculate_preflop_percentage(self, player_hand, dealer_hand):
        player_strength = self.calculate_preflop_strength(player_hand)
        dealer_strength = self.calculate_preflop_strength(dealer_hand)
        final_ev_player = player_strength / (player_strength + dealer_strength)
        final_ev_dealer = dealer_strength / (player_strength + dealer_strength)
        formated_res_player = "{:.1f}".format(final_ev_player * 100)
        formated_res_dealer = "{:.1f}".format(final_ev_dealer * 100)
        print("Player Win Percent:" + " " +  str(formated_res_player) + "%")
        print("Dealer Win Percent:" + " " +  str(formated_res_dealer) + "%")


    def initial_flop(self):
        if len(self.cards_on_table) == 0:
            for i in range(3):
                self.cards_on_table.append(self.deck.pop())
        print("Player Win Percent:" + " " +  str(self.calculate_win_percentage_player()) + "%")
        print("Dealer Win Percent:" + " " +  str(self.calculate_win_percentage_dealer()) + "%")
    
        self.update_hand_probabilities()

    def draw_fourth(self):
        if len(self.cards_on_table) == 3:
            self.cards_on_table.append(self.deck.pop())
        print("Player Win Percent:" + " " +  str(self.calculate_win_percentage_player()) + "%")
        print("Dealer Win Percent:" + " " +  str(self.calculate_win_percentage_dealer()) + "%")

        self.update_hand_probabilities()

    def draw_river(self):
        if len(self.cards_on_table) == 4:
            self.cards_on_table.append(self.deck.pop())

        player_strength = self.evaluate_final_hand(self.drawn_player)
        dealer_strength = self.evaluate_final_hand(self.drawn_dealer)

        if player_strength > dealer_strength:
            print("Player Win Percent: 100%")
            print("Dealer Win Percent: 0%")
        elif dealer_strength > player_strength:
            print("Player Win Percent: 0%")
            print("Dealer Win Percent: 100%")
        else:
            print("Player Win Percent: 50%")
            print("Dealer Win Percent: 50%")

# These are hard coded values that will need to be replaced by the inverse probability of each hitting each hand
    def calculate_hand_value(self, hand):
        if self.has_royal_flush(hand):
            return 10
        elif self.has_straight_flush(hand):
            return 9
        elif self.has_four_of_a_kind(hand):
            return 8
        elif self.has_full_house(hand):
            return 7
        elif self.has_flush(hand):
            return 6
        elif self.has_straight(hand):
            return 5
        elif self.has_three_of_a_kind(hand):
            return 4
        elif self.has_two_pair(hand):
            return 3
        elif self.has_pair(hand):
            return 2
        else:
            return 1

    def eval_hand(self, hand, cards_on_table, remaining_deck):
        EV_total = 0
        remaining_cards = len(remaining_deck)

        # All combinations of the next card (stage) from the remaining deck
        for next_card in combinations(remaining_deck, 1):
            hypothetical_hand = hand + list(next_card)
            full_hand = hypothetical_hand + cards_on_table

            hand_value = self.calculate_hand_value(full_hand)

            probability = 1 / self.combination(remaining_cards, 1)

            EV_total += probability * hand_value

        return EV_total
    
    def eval_hand_player(self):
        player_hand = self.drawn_player + self.cards_on_table
        return self.eval_hand(player_hand, self.cards_on_table, self.deck)

    def eval_hand_dealer(self):
        dealer_hand = self.drawn_dealer + self.cards_on_table
        return self.eval_hand(dealer_hand, self.cards_on_table, self.deck)

    def calculate_win_percentage_player(self):
        ev_player = self.eval_hand_player()
        ev_dealer = self.eval_hand_dealer()
        
        total_ev = ev_player + ev_dealer
        win_percentage = ev_player / total_ev if total_ev > 0 else 0
        return "{:.1f}".format(win_percentage * 100)
    
    def calculate_win_percentage_dealer(self):
        ev_player = self.eval_hand_player()
        ev_dealer = self.eval_hand_dealer()

        total_ev = ev_player + ev_dealer
        win_percentage = ev_dealer / total_ev if total_ev > 0 else 0
        return "{:.1f}".format(win_percentage * 100)
    
    def evaluate_final_hand(self, hand):
        combined_hand = hand + self.cards_on_table
        full_hand_value = self.calculate_hand_value(combined_hand)
        return full_hand_value


    # Credit to Brian Caffey for inspiration for the following functions
    # https://briancaffey.github.io/2018/01/02/checking-poker-hands-with-python.html/
    # And to the following StackOverflow post for the Ace-low straight flush special case
    # https://poker.stackexchange.com/questions/4350/can-an-ace-be-low-in-a-straight

    def has_royal_flush(self, hand):
        suit_groups = defaultdict(list)
        # Check for group of 5 cards in the same suit
        for card in hand:
            suit_groups[card[1]].append(card[0])

        royal_flush_set = set(self.values[-5:])  # Last five elements (10, J, Q, K, A)
        for suit, values in suit_groups.items():
            # Check if all royal flush cards are present
            if royal_flush_set.issubset(set(values)):
                return True
        return False

    def has_straight_flush(self, hand):
        suit_groups = defaultdict(list)
        for card in hand:
            suit_groups[card[1]].append(self.values.index(card[0]))

        # Check for valid straight flush in each suit_group
        for suit, ranks in suit_groups.items():
            # Check for Ace-low straight, if Ace is present then it can also be low
            if 12 in ranks:
                ranks.append(0)

            unique_ranks = sorted(set(ranks))

            for i in range(len(unique_ranks) - 4):
                if unique_ranks[i + 4] - unique_ranks[i] == 4:
                    return True
        return False

    def has_four_of_a_kind(self, hand):
        values = [card[0] for card in hand]
        value_counts = Counter(values)
        return 4 in value_counts.values()

    def has_full_house(self, hand):
        values = [card[0] for card in hand]
        value_counts = Counter(values)

        # Check for three of a kind and pair, check if they are different suits
        if self.has_three_of_a_kind(hand) and self.has_pair(hand):
            for suit, count in value_counts.items():
                if count == 3:
                    three_kind_suit = suit
                    break
            for suit, count in value_counts.items():
                if count == 2 and suit != three_kind_suit:
                    return True
        return False

    def has_flush(self, hand):
        suits = [card[1] for card in hand]
        suit_counts = Counter(suits)
        return 5 in suit_counts.values()

    def has_straight(self, hand):
        values = [card[0] for card in hand]
        rank_indices = [self.values.index(v) for v in values]
        # Check for Ace-low straight, if Ace is present then it can also be low
        if 12 in rank_indices:
            rank_indices.append(0)

        unique_indices = sorted(set(rank_indices))

        for i in range(len(unique_indices) - 4):
            if unique_indices[i + 4] - unique_indices[i] == 4:
                return True
        return False

    def has_three_of_a_kind(self, hand):
        values = [card[0] for card in hand]
        value_counts = Counter(values)
        return 3 in value_counts.values()

    def has_two_pair(self, hand):
        values = [card[0] for card in hand]
        value_counts = Counter(values)
        return len([v for v in value_counts.values() if v == 2]) == 2

    def has_pair(self, hand):
        values = [card[0] for card in hand]
        value_counts = Counter(values)
        return 2 in value_counts.values()

    def high_card(self, hand):
        values = [card[0] for card in hand]
        # index face_cards in order of value (Ace high)
        face_cards = ['A', 'K', 'Q', 'J']

        high_cards = [card for card in values if card in face_cards]
        if high_cards:
            return max(high_cards, key=lambda card: face_cards.index(card))
        else:
            return False
        

    # This section is to dynamically update the dictionary of hand probabilities
    # This will be used to plot the probabilities of each hand at each stage of 
    # the game we want to show the probability of achieving any hand
    # Only run on the player's hand, not the dealer's

    def update_hand_probabilities(self):
        self.hand_data['Pair'] = self.estimate_probability_of_pair(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['2Pair'] = self.estimate_probability_of_two_pair(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['3Kind'] = self.estimate_probability_of_three_kind(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['Str'] = self.estimate_probability_of_straight(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['Flush'] = self.estimate_probability_of_flush(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['FH'] = self.estimate_probability_of_full_house(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['SF'] = self.estimate_probability_of_straight_flush(self.drawn_player, self.cards_on_table, self.deck)
        self.hand_data['RF'] = self.estimate_probability_of_royal_flush(self.drawn_player, self.cards_on_table, self.deck)
        self.plot_probabilities()

    def estimate_probability_of_pair(self, hand, cards_on_table, remaining_deck):
        if self.has_pair(hand + cards_on_table):
            return 1.0

        pair_probability = 0.0
        for card in remaining_deck:
            if any(card[0] == existing_card[0] for existing_card in hand + cards_on_table):
                pair_probability += 1 / len(remaining_deck)
        return pair_probability
    
    def estimate_probability_of_two_pair(self, hand, cards_on_table, remaining_deck):
        if self.has_two_pair(hand + cards_on_table):
            return 1.0

        two_pair_probability = 0.0
        combined_hand = hand + cards_on_table
        value_counts = Counter(card[0] for card in combined_hand)

        if any(count >= 2 for count in value_counts.values()):
            for card in remaining_deck:
                hypothetical_hand = combined_hand + [card]
                if self.has_two_pair(hypothetical_hand):
                    two_pair_probability += 1 / len(remaining_deck)

        return two_pair_probability
    
    def estimate_probability_of_three_kind(self, hand, cards_on_table, remaining_deck):
        if self.has_three_of_a_kind(hand + cards_on_table):
            return 1.0
        
        three_kind_probability = 0.0
        combined_hand = hand + cards_on_table

        for card in remaining_deck:
            hypothetical_hand = combined_hand + [card]
            if self.has_three_of_a_kind(hypothetical_hand):
                three_kind_probability += 1 / len(remaining_deck)

        return three_kind_probability

    def estimate_probability_of_straight(self, hand, cards_on_table, remaining_deck):
        if self.has_straight(hand + cards_on_table):
            return 1.0
        
        straight_probability = 0.0
        combined_hand = hand + cards_on_table

        for card in remaining_deck:
            hypothetical_hand = combined_hand + [card]
            if self.has_straight(hypothetical_hand):
                straight_probability += 1 / len(remaining_deck)

        return straight_probability

    def estimate_probability_of_flush(self, hand, cards_on_table, remaining_deck):
        if self.has_flush(hand + cards_on_table):
            return 1.0
        
        flush_probability = 0.0
        combined_hand = hand + cards_on_table

        for card in remaining_deck:
            hypothetical_hand = combined_hand + [card]
            if self.has_flush(hypothetical_hand):
                flush_probability += 1 / len(remaining_deck)

        return flush_probability

    def estimate_probability_of_full_house(self, hand, cards_on_table, remaining_deck):
        if self.has_full_house(hand + cards_on_table):
            return 1.0
        
        fh_probability = 0.0
        combined_hand = hand + cards_on_table

        for card in remaining_deck:
            hypothetical_hand = combined_hand + [card]
            if self.has_full_house(hypothetical_hand):
                fh_probability += 1 / len(remaining_deck)

        return fh_probability

    def estimate_probability_of_straight_flush(self, hand, cards_on_table, remaining_deck):
        if self.has_straight_flush(hand + cards_on_table):
            return 1.0
        
        sf_probability = 0.0
        combined_hand = hand + cards_on_table

        for card in remaining_deck:
            hypothetical_hand = combined_hand + [card]
            if self.has_straight_flush(hypothetical_hand):
                sf_probability += 1 / len(remaining_deck)

        return sf_probability

    def estimate_probability_of_royal_flush(self, hand, cards_on_table, remaining_deck):
        if self.has_royal_flush(hand + cards_on_table):
            return 1.0
        
        rf_probability = 0.0
        combined_hand = hand + cards_on_table

        for card in remaining_deck:
            hypothetical_hand = combined_hand + [card]
            if self.has_royal_flush(hypothetical_hand):
                rf_probability += 1 / len(remaining_deck)

        return rf_probability

    def plot_probabilities(self):
        hands = list(self.hand_data.keys())
        winning_odds = list(self.hand_data.values())

        plt.figure(figsize=(12, 7))
        plt.bar(hands, winning_odds, color='green', width=.8)
        plt.xlabel("Possible Hands")
        plt.ylabel("Odds of Achieving Hand")
        plt.show()