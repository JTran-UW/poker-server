from random import choice

class Table:
    def __init__(self):
        self.table = list()

    def show_card(self, temp_cards, n):
        """
        Pick and show random n cards
        temp_cards: the set of cards to choose
        n: the number of cards to choose
        return: [chosen cards, the remaining set of cards]
        """
        choices = list()

        for num in range(n):
            c = choice(temp_cards)
            temp_cards.remove(c)
            self.table.append(c)
            choices.append(c)
        
        self.cards = temp_cards
        return [choices, temp_cards]
