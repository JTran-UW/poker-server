from random import sample
from itertools import combinations

class Player:
    def __init__(self, name):
        """
        Initialize a player with a balance of $10,000
        """
        self.name = name
        self.status = True
        self.balance = 10000
        self.bet = 0

    def get_cards(self, temp_cards):
        """
        Picks out a hand from temp_cards
        temp_cards: All cards that are still available to be held (type: list)
        Return: None
        """
        # Pick out the cards
        card1, card2 = sample(temp_cards, 2)
        self.hand = [card1, card2]
        
        # Players cannot have the same card
        temp_cards.remove(card1)
        temp_cards.remove(card2)

        return temp_cards

    def hand_value(self, table):
        self.cards = table + self.hand

        # All combinations of 5 cards
        combos = list(combinations(self.cards, 5))
        values = dict()

        # Evaluate each hand
        for combo in combos:
            # Important variables
            combo_nums = [card.face for card in combo]
            combo_suits = [card.suit for card in combo]
            high_card = max(combo_nums)
            rep_count = [combo_nums.count(num) for num in set(combo_nums)]
            order = range(min(combo_nums), max(combo_nums))

            # Hands
            straight = sorted(combo_nums) == list(order)
            flush = len(set(combo_suits)) == 1
            four_of_a_kind = 4 in rep_count
            full_house = 3 in rep_count and 2 in rep_count
            three_of_a_kind = 3 in rep_count
            two_pair = rep_count.count(2) == 2
            pair = 2 in rep_count

            # Hand value
            if straight and flush:
                values[800 + high_card] = combo
                top_hand = "straight-flush"
            elif four_of_a_kind:
                values[700 + high_card] = combo
                top_hand = "four-of-a-kind"
            elif full_house:
                values[600 + high_card] = combo
                top_hand = "full-house"
            elif flush:
                values[500 + high_card] = combo
                top_hand = "flush"
            elif straight:
                values[400 + high_card] = combo
                top_hand = "straight"
            elif three_of_a_kind:
                values[300 + high_card] = combo
                top_hand = "three-of-a-kind"
            elif two_pair:
                values[200 + high_card] = combo
                top_hand = "two-pair"
            elif pair:
                values[100 + high_card] = combo
                top_hand = "pair"
            else:
                values[high_card] = combo
                top_hand = f"{high_card} high"
        
        # Determine the best combo
        top_hand_key = max(values.keys())
        top_combo = values[top_hand_key]
        top_combo = [card.name for card in top_combo]

        return [top_hand_key, top_hand, top_combo]

    def zero_bets(self):
        """
        Zero out bet
        """
        self.bet = 0

    def update_balance(self, amount):
        """
        Have player gain or lose some amount of money
        amount: amount to change balance by, positive for gain, negative for loss (type: int or float)
        Return: None
        """
        self.balance += amount

    def fold(self):
        """
        Player may fold, sets them to inactive and deletes their hand
        Return: None
        """
        self.status = False
        self.hand = []
