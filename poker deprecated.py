# ================================================ IMPORTS AND VAR DEFINTIONS =============================== #
from random import sample, randint, choice
from itertools import combinations
from collections import deque


# All cards that exist
cards = [[1, 'hearts'], [1, 'clubs'], [1, 'spades'], [1, 'diamonds'], [2, 'hearts'], [2, 'clubs'], [2, 'spades'], [2, 'diamonds'], [3, 'hearts'], [3, 'clubs'], [3, 'spades'], [3, 'diamonds'], [4, 'hearts'], [4, 'clubs'], [4, 'spades'], [4, 'diamonds'], [5, 'hearts'], [5, 'clubs'], [5, 'spades'], [5, 'diamonds'], [6, 'hearts'], [6, 'clubs'], [6, 'spades'], [6, 'diamonds'], [7, 'hearts'], [7, 'clubs'], [7, 'spades'], [7, 'diamonds'], [8, 'hearts'], [8, 'clubs'], [8, 'spades'], [8, 'diamonds'], [9, 'hearts'], [9, 'clubs'], [9, 'spades'], [9, 'diamonds'], [10, 'hearts'], [10, 'clubs'], [10, 'spades'], [10, 'diamonds'], [11, 'hearts'], [11, 'clubs'], [11, 'spades'], [11, 'diamonds'], [12, 'hearts'], [12, 'clubs'], [12, 'spades'], [12, 'diamonds'], [13, 'hearts'], [13, 'clubs'], [13, 'spades'], [13, 'diamonds']]
temp_cards = cards # Cards that may be played

blinds = [100, 200]
player_names = ["Larry", "Joe", "Moe"]
group = dict()
pot = 0
table = list()
folded = list()
hands = list()

# Global variables for dealer, small blind, big blind indexes
dealer = int()
small_blind = int()
big_blind = int()

# -============================================ CLASS DEFINITIONS ==================================== #

class player:
    def __init__(self, name, order, role):
        """
        Initialize a player with a balance of $10,000
        """
        self.name = name
        self.order = order
        self.role = role
        self.status = "Active"
        self.balance = 10000
        self.bet = 0
    def get_cards(self):
        """
        Picks out a hand from temp_cards \n
        Return: None
        """
        # Pick out the cards
        card1, card2 = sample(temp_cards, 2)
        self.hand = [card1, card2]
        hands.append(self.hand)

        # Players cannot have the same card
        temp_cards.remove(card1)
        temp_cards.remove(card2)
    def update_balance(self, amount):
        """
        Have player gain or lose some amount of money
        amount: amount to change balance by, positive for gain, negative for loss (type: int or float)
        Return: None
        """
        try:
            self.balance += amount
        except TypeError:
            print("Unusable amount given.")
    def fold(self):
        """
        Player may fold, sets them to inactive and deletes their hand
        Return: None
        """
        self.status = "Inactive"
        self.hand = []

class card:
    def __init__(self, face, suit):
        """
        Write card class
        """
        self.face = face
        self.suit = suit

        # Write name
        if self.face == 11:
            self.face_name = "Jack"
        elif self.face == 12:
            self.face_name = "Queen"
        elif self.face == 13:
            self.face_name = "King"
        elif self.face == 1:
            self.face_name = "Ace"
        else:
            self.face_name = self.face
        self.name = f"{self.face_name} of {self.suit}"

# ==================================================== FUNCTION DEFINITIONS =================================== #

def decide_blinds(dealer, num):
    """
    Receives a dealer by their index in player_names + 1, the number of players, updates roles accordingly
    dealer: index of dealer in player_names + 1 (type: int)
    num: Number of players (type: int)
    Return: tuple, containing indexes of small blind and big blind (type: tuple)
    """
    for i, name in enumerate(player_names): # Initialize players
        # To the right of the dealer is the small blind, to the right of them big blind
        if dealer == i:
            group[name] = player(name, dealer + 1, "Dealer")
        elif (dealer + 1) % num == i:
            group[name] = player(name, i + 1, "Small blind")
            small = i
        elif (dealer + 2) % num == i:
            group[name] = player(name, i + 1, "Big blind")
            big = i
        else:
            group[name] = player(name, i + 1, "None")
    return (small, big)

def call_raise(player, ante):
    while True:
        if ante >= player.balance:
            init_in = input(f"Go all-in [Y/N] (If no, you will fold)? ").lower()
            if init_in == "y":
                balance = player.balance
                player.bet = balance
                player.update_balance(-player.balance)
                return "all-in"
            elif init_in == "n":
                return "fold"
            else:
                print("Input not understood.")
        else:
            init_in = input(f"Would you like to 'call' or 'raise' or 'fold' (ante: {ante})? ").lower()
            if init_in == "call":
                # Deduct enough to meet ante
                player.bet = ante
                player.update_balance(-player.bet)
                return "call"
            elif init_in == "raise":
                raise_in = int(input("How much would you like to raise by? "))
                player.bet += raise_in
                player.update_balance(-player.bet)
                return ("raise", raise_in)
            elif init_in == "fold":
                return "fold"
            else:
                print("Input not understood.")

def check_bet(player):
    while True:
        init_in = input("Would you like to 'check' or 'bet' or 'fold'? ")
        if init_in == "check":
            return "check"
        elif init_in == "bet":
            bet_in = int(input("How much would you like to bet by? "))
            player.bet = bet_in
            group[player].update_balance(-group[player].bet)
            return ("bet", bet_in)
        elif init_in == "fold":
            return "fold"
        else:
            print("Input not understood.")

def straight_check(card_nums):
    return sorted(card_nums) == list(range(min(card_nums), max(card_nums) + 1)) # Checks if the card numbers produce a straight

def flush_check(suits):
    return len(set(suits)) == 1 # Checks if the card suits produce a flush

def four_of_a_kind_check(rep_count):
    return 4 in rep_count # If four-of-a-kind, then there would be 4 instances of some card num

def full_house_check(rep_count):
    return 3 in rep_count and 2 in rep_count

def three_of_a_kind_check(rep_count):
    return 3 in rep_count

def two_pair_check(rep_count):
    return rep_count.count(2) == 2

def pair_check(rep_count):
    return 2 in rep_count

def who_won(table, hands):
    """
    Determine which player had a better hand
    table: dealt cards on table (type: list)
    hands: cards dealt to each player (type: list)
    return: index of player who won (type: int), if tie, list of indices of all tied players (type: list)
    """
    hands = hands
    winner = [0] * len(hands)

    # Add table cards to hands
    for i, hand in enumerate(hands):
        for card in table:
            hands[i].append(card)

    # Score each hand
    for i, hand_iter in enumerate(hands):
        hand_nums = [card[0] for card in hand_iter]
        five_combo = list(combinations(hand_iter, 5)) # Get all combinations of 5 cards
        value = list() # Contains values of all hand combinations
        value_tie = list() # Contains values of all tie-breaking combinations

        if group[player_names[i]].status == "Active":
            for combo in five_combo:
                # Define some useful variables
                card_nums = [combo[0][0], combo[1][0], combo[2][0], combo[3][0], combo[4][0]] # This combination's card numbers
                rep_count = [card_nums.count(num) for num in set(card_nums)]
                suits = [combo[0][1], combo[1][1], combo[2][1], combo[3][1], combo[4][1]] # This combination's suits

                # Perform checks
                straight = straight_check(card_nums)
                flush = flush_check(suits)
                four_of_a_kind = four_of_a_kind_check(rep_count)
                full_house = full_house_check(rep_count)
                three_of_a_kind = three_of_a_kind_check(rep_count)
                two_pair = two_pair_check(rep_count)
                pair = pair_check(rep_count)

                # Update 'value' to keep track of each combination's value
                if straight and flush:
                    value.append("straight-flush")
                    value_tie.append(max(card_nums))
                elif four_of_a_kind:
                    value.append("four-of-a-kind")
                    value_tie.append(max(set(card_nums), key=card_nums.count)) # Get the mode of the card numbers
                elif full_house:
                    value.append("full-house")
                    # TODO Finish the hand ranking!
                elif flush:
                    value.append("flush")
                elif straight:
                    value.append("straight")
                elif three_of_a_kind:
                    value.append("three-of-a-kind")
                elif two_pair:
                    value.append("two-pair")
                elif pair:
                    value.append("pair")
                else:
                    value.append("high-card")
        
        print(f"{player_names[i]} ({group[player_names[i]].hand}) has: ")
        # Evaluate what was collected in 'value'
        if "straight-flush" in value:
            winner.append([800, max(hand_nums)])
            print("Straight-flush")
        elif "four-of-a-kind" in value:
            winner.append([700, max(hand_nums)])
            print("Four of a kind")
        elif "full-house" in value:
            winner.append([600, max(hand_nums)])
            print("Full house")
        elif "flush" in value:
            winner.append([500, max(hand_nums)])
            print("Flush")
        elif "straight" in value:
            winner.append([400, max(hand_nums)]) # TODO a higher straight/three-of-a-kind/other hand can win
            print("Straight")
        elif "three-of-a-kind" in value:
            winner.append([300, max(hand_nums)])
            print("Three of a kind")
        elif "two-pair" in value:
            winner.append([200, max(hand_nums)])
            print("Two pair")
        elif "pair" in value:
            winner.append([100, max(hand_nums)])
            print("Pair")
        elif "high-card" in value:
            winner.append([0, max(hand_nums)])
            print(f"High card of {max(hand_iter)[0]}")
        else:
            print("Player folded.")
            winner.append([-1, -1])
    
    # Determine the winner
    winner_pure = [val[0] for val in winner]
    tie_pure = [val[1] for val in winner]
    if winner_pure.count(max(winner_pure)) == 1:
        return winner_pure.index(max(winner_pure))
    else:
        tie_breaker = [val[1] for val in winner if val[0] == max(winner_pure)]
        if tie_breaker.count(max(tie_breaker)) == 1: # If there's a tie
            return tie_pure.index(max(tie_breaker))
        else:
            return [i for i, val in enumerate(tie_pure) if val in tie_breaker and winner[i][0] == max(winner_pure)] # Return a list containing the tied players' indices

def run_round(first):
    global dealer, small_blind, big_blind, pot, table, folded

    # Decide the dealer, small blind, big blind
    num = len(player_names)
    if first:
        # Determine the first dealer randomly
        dealer = randint(0, num - 1)
        small_blind, big_blind = decide_blinds(dealer, num)
        small_player = group[player_names[small_blind]]
        big_player = group[player_names[big_blind]]

        # Small blind and big blind pay something
        small_player.bet = blinds[0]
        big_player.bet = blinds[1]
        for name in player_names:
            print(f"{name} is the {group[name].role}")

        # Set initial ante
        ante = blinds[1]
    else:
        # Determine the new dealer
        dealer += 1
        small_blind, big_blind = decide_blinds(small_blind, num) # TODO The small blind and big blind must pay some amount
        small_player = group[player_names[small_blind]]
        big_player = group[player_names[big_blind]]

        # Small blind and big blind pay something
        small_player.bet = blinds[0]
        big_player.bet = blinds[1]
        for name in player_names:
            print(f"{name} is the {group[name].role}")

        # Set initial ante
        ante = 0
    
    # Deal cards
    for person in player_names:
        group[person].get_cards()

    round_num = 1
    # Run one round
    while True:
        # Run betting
        if round_num == 1:
            to_pay = deque(group.values())
            to_pay.rotate((len(player_names) + 1) - (big_blind + 2)) # The person who is after the big blind bets first.
            to_pay = list(to_pay)
        else:
            to_pay = deque([person for person in group.values() if person.status == "Active"])
            to_pay.rotate((len(player_names)) + 1 - (big_blind + 2))
            to_pay = list(to_pay)

        while len(to_pay) > 0:
            for person in to_pay:
                print(f"{person.name}'s turn.'")
                if person.bet == ante:
                    user_in = check_bet(person)
                else:
                    user_in = call_raise(person, ante)
                try:
                    ante += user_in[1]
                except TypeError:
                    if user_in == "fold":
                        person.status = "Inactive"
                        folded.append(True)
                if user_in[0] == "raise" or user_in[0] == "bet":
                    print(f"{person.name} {user_in[0]}s.") # TODO IF a person loses all their money, they go all-in
                elif user_in == "all-in":
                    print(f"{person.name} goes all-in")
                else:
                    print(f"{person.name} {user_in}s.")
                if len(folded) == len(player_names) - 1:
                    # TODO Whoever's left wins!
                    pass
            bets = [group[person].bet==ante for person in player_names] # All people who have paid the bet are True, all who have not are False
            to_pay = [group[player_names[i]] for i, var in enumerate(bets) if var == False and group[player_names[i]].status == "Active"] # Player classes who have not paid the bet.

        # Update what's in the pot
        pot += sum([group[person].bet for person in player_names])

        # Zero everyone's bets, subtract money from their balance
        for person in player_names:
            group[person].bet = 0
        
        # Show cards
        if round_num == 3: # Determine the winner of the game
            # Put out last card
            card = choice(temp_cards)
            table.append(card)
            print(f"The 5th street: {table[-1]}")
            temp_cards.remove(card)

            # Run the winner function
            win = who_won(table, hands)
            if type(win) == list:
                tie_str = ", ".join([player_names[i] for i in win]) # Write a string based on the player names of who tied
                print(f"Tie between {tie_str}")
                for winner in win:
                    group[player_names[winner]].update_balance(int(pot/len(win)))
            else:
                print(f"The winner is {player_names[win]}")
                print(pot)
                group[player_names[win]].update_balance(pot) # Person who won.balance += pot
            break
        elif round_num == 1: # The flop
            table = sample(temp_cards, 3)
            print(f"The flop: {table[0]} {table[1]} {table[2]}")
            for card in table:
                temp_cards.remove(card)
        else:
            card = choice(temp_cards)
            table.append(card)
            print(f"The 4th street: {table[-1]}")
            temp_cards.remove(card)

        # Zero out the ante
        ante = 0

        # Increase the round number
        round_num += 1
# TODO Make everyone active again, zero out the folded variable and pot

# ====================================== MAIN PROGRAM ================================== #


run_round(True)
balances = [group[name].balance for name in player_names]
print(balances)