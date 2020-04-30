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
nums = [0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8]
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
    print(f"\nRound #{g.round_num}")

    # Important variables
    if g.round_num == 1:
        ante = b[1]
    else:
        ante = 0
    g.round_num += 1
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

        print(f"\nThe {show_name}: ", end="")
        for i, card in enumerate(choices):
            if i == len(choices) - 1:
                print(card.name)
            else:
                print(card.name, end=", ")
    
    # Zero the bets
    for person in active:
        person.zero_bets()

# ====================================================== STAGE 4: DETERMINE THE WINNER ======================================================

print("\n")

# For a fold-out
if len(active) == 1:
    winner = active[0]

# Go to the hands for a decision
else:
    contenders = dict()

    for player in active:
        # Get each players hand values
        hand = player.hand_value(t.table)
        contenders[hand[0]] = player

        # Print the hand values
        print(f"{player.name} has {hand[1]} (", end="")
        for card in hand[2][:-1]:
            print(card, end=", ")
        print(f"{hand[2][-1]})")
    
    # Determine who had the best hand
    winner_key = max(contenders.keys())
    winner = contenders[winner_key]

# Print the winner
print(f"{winner.name} wins the hand!")
