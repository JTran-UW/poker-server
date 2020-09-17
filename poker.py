from game import Game
from table import Table

# ===================================================== STAGE 1: SETUP ===========================================

# Activate game
g = Game()
t = Table()
not_paid = g.start_round(True)
cards = g.cards
active = not_paid
all_in = list()

# =================================================== STAGE 2: PLAY ONE ROUND ==========================================================

# Keep playing rounds while the 5th street hasn't been shown / there are more than 1 players
while g.round_num < 5 and len(active) > 1:
    print(f"\nRound #{g.round_num}")

    # Important variables
    if g.round_num == 1:
        ante = g.blinds[1]
    else:
        ante = 0
    g.round_num += 1
    not_paid = [person for person in active if person not in all_in]

    # ================================================== STAGE 3: RUN BETTING =============================================================
    while len(not_paid) > 0:

        # Run betting
        betting = g.run_betting(ante, not_paid)
        active = betting["active"]
        all_in = betting["all_in"]
        not_paid = betting["not_paid"]
        ante = betting["ante"]

        # Player who haven't folded / paid the ante
        not_paid = [person for person in active if person in not_paid]
        not_paid = [person for person in not_paid if person not in all_in]

    # Divide up the pot
    payments = list(set([person.bet for person in active]))
    g.pot_payments(payments, active)

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

# Remove placeholder pot
g.pots.pop(0)

# For a fold-out
if len(active) == 1:
    winner = active[0]
    pot_total = sum([pot.amount for pot in g.pots])
    print(f"{winner.name} wins {pot_total}")

# Go to the hands for a decision
else:
    # Loop through pots
    for i, pot in enumerate(g.pots):
        print(f"Pot #{i + 1}")
        contenders = dict()
        eligible = [player for player in active if player in pot.assoc_ps]

        for player in eligible:
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

        # Update balances
        pot_total = pot.amount
        winner.update_balance(pot_total)

        print(f"{winner.name} wins ${pot_total}!")
