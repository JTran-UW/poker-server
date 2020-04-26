from random import sample

class Player:
    def __init__(self, name):
        """
        Initialize a player with a balance of $10,000
        """
        self.name = name
        self.status = "Active"
        self.balance = 10000
        self.bet = 0
    def get_cards(self, temp_cards, hands):
        """
        Picks out a hand from temp_cards
        temp_cards: All cards that are still available to be held (type: list)
        hands: All hands in play (type: list)
        Return: None
        """
        # Pick out the cards
        card1, card2 = sample(temp_cards, 2)
        self.hand = [card1, card2]
        hands.append(self.hand)

        # Players cannot have the same card
        temp_cards.remove(card1)
        temp_cards.remove(card2)
    def zero_bets(self):
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
        self.status = "Inactive"
        self.hand = []