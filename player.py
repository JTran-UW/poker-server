from random import sample

class Player:
    def __init__(self, name):
        """
        Initialize a player with a balance of $10,000
        """
        self.name = name
        self.status = True
        self.balance = 10000
        self.bet = 0

        # Hand frequencies
        self.one

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
        self.suits = [card.suit for card in self.cards]
        self.faces = [card.face for card in self.cards]

        # All hand checks
        self.flush = 3# TODO FINSIH CHECKS


        # Check for straight-flush
        if self.flush:
            pass

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
