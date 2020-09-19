from game import Game
from table import Table

# Setup

# Activate game
poker = Game()
table = Table()
not_paid = poker.start_round(True)
cards = poker.cards
active = not_paid
all_in = list()

# Play one round

# Keep playing rounds while the 5th street hasn't been shown / there are more than 1 players
while poker.round_num < 5 and len(active) > 1:
    print(f"\nRound #{poker.round_num}")

    # Important variables
    if poker.round_num == 1:
        ante = poker.blinds[1]
    else:
        ante = 0
    poker.round_num += 1
    not_paid = [person for person in active if person not in all_in]

    # Run betting

    while len(not_paid) > 0:

        # Run betting
        betting = poker.run_betting(ante, not_paid)
        active = betting["active"]
        all_in = betting["all_in"]
        not_paid = betting["not_paid"]
        ante = betting["ante"]

        # Player who haven't folded / paid the ante
        not_paid = [person for person in active if person in not_paid]
        not_paid = [person for person in not_paid if person not in all_in]

    # Divide up the pot
    payments = list(set([person.bet for person in active]))
    poker.pot_payments(payments, active)

    # Get the cards to table
    if poker.round_num == 2:
        show = table.show_card(cards, 3)
        show_name = "flop"
    elif poker.round_num == 3:
        show = table.show_card(cards, 1)
        show_name = "turn"
    elif poker.round_num == 4:
        show = table.show_card(cards, 1)
        show_name = "river"

    # Print the cards
    if poker.round_num < 5:
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

# Determine the winner

print("\n")

# Remove placeholder pot
poker.pots.pop(0)

# For a fold-out
if len(active) == 1:
    winner = poker.fold_out(active[0])

# Go to the hands for a decision
else:
    winner = poker.determine_winner(table, active)

print(winner)
