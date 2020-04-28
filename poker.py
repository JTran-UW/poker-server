from card import Card
from game import Game
from player import Player
from table import Table

# ===================================================== STAGE 1: SETUP ===========================================

# Generate players
names = ["Larry", "Moe", "Eric", "Joe"]
p = list()
for name in names:
    p.append(Player(name))

# Generate cards
nums = list(range(2, 15))
suits = ["diamonds", "hearts", "spades", "clubs"]
cards = list()

for num in nums:
    for suit in suits:
        cards.append(Card(num, suit))

# Blinds
b = (100, 200)

# Activate game
g = Game(p, cards)
t = Table()
not_paid = g.start_round(True, b)
cards = g.cards
active = not_paid

# =================================================== STAGE 2: PLAY ONE ROUND ==========================================================

# Keep playing rounds while the 5th street hasn't been shown / there are more than 1 players
while g.round_num < 5 and len(active) > 1:
    print(f"Round #{g.round_num}")

    # Important variables
    ante = b[1]
    not_paid = active

    # ================================================== STAGE 3: RUN BETTING =============================================================
    while len(not_paid) > 0:

        # Run betting
        betting = g.run_betting(ante, not_paid)
        active = betting["active"]
        not_paid = betting["not_paid"]
        ante = betting["ante"]

        # Player who haven't folded / paid the ante
        not_paid = [person for person in active if person in not_paid]
    
    # Get the cards to table
    if g.round_num == 2:
        show = t.show_card(cards, 3)
        show_name = "flop"
    elif g.round_num == 3:
        show = t.show_card(cards, 1)
        show_name = "turn"
    elif g.round_num == 4:
        show = t.show_card(cards, 1)
        show_name = "river"

    # Print the cards
    if g.round_num < 5:
        choices = show[0]
        cards = show[1]

        print(f"The {show_name}: ", end="")
        for card in choices:
            print(card.name, end=", ")
        

# ====================================================== STAGE 4: DETERMINE THE WINNER ======================================================

# For a fold-out
if len(active) == 1:
    winner = active[0]
else:
    contenders = dict()

    for player in active:
        hand = player.hand_value(t.table)
        contenders[hand[0]] = player

        print(f"{player.name} has {hand[1]} ({hand[2]})")
    
    winner_key = max(contenders.keys())
    winner = contenders[winner_key]

print(f"{winner.name} wins the hand!")
