from random import choice

class Table:
    def __init__(self):
        self.table = list()

    def show_card(self, temp_cards, n):
        choices = list()

        for num in range(n):
            c = choice(temp_cards)
            temp_cards.remove(c)
            self.table.append(c)
            choices.append(c)
        
        self.cards = temp_cards
        return [choices, temp_cards]
