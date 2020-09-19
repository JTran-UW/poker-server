from game import Game

# Activate game
poker = Game()
active = poker.run_round()
print()

# Find the winner
if len(active) == 1:
    winner = poker.fold_out(active[0])
else:
    winner = poker.determine_winner(active)

# Print the winner
print(winner)
