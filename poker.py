from card import Card
from game import Game
from player import Player


names = ["Larry", "Moe", "Eric", "Joe"]
p = list()
for name in names:
    p.append(Player(name))

# Blinds
b = (100, 200)

g = Game(p, [])
playing = g.start_round(True, b)

#while g.round_num < 5 and len(playing) > 1: # Keep playing rounds while the 5th street hasn't been shown / there are more than 1 players
#    print(f"Round #{g.round_num}")

# Important variables
ante = b[1]
new_ante = ante + 1
not_paid = playing

# Run betting with all those who haven't paid
while len(not_paid) > 0:
    betting = g.run_betting(ante, not_paid)
    active = betting["active"] # Players who are still active (haven't folded)
    not_paid = betting["not_paid"] # Players who haven't paid the ante
    ante = betting["ante"] # Ante as seen from the round of betting

    print([person.name for person in active])
    print([person.name for person in not_paid])
    not_paid = list(set.intersection(set(active), set(not_paid))) # Player who haven't folded / paid the ante


#    print("\n")
