from random import randint
from player import Player
from pot import Pot
from card import Card
from table import Table

class Game:
    def __init__(self):
        """
        Create a game \n
        players: list of players, of type player class (type: list) \n
        cards: list of all playable cards
        """
        self.players = [Player("Larry"), Player("Moe"), Player("Eric"), Player("Joe")]
        self.player_count = len(self.players)
        self.cards = []
        self.round_num = 1
        self.pots = [Pot()]
        self.pots_i = 0
        self.blinds = (100, 200)
        self.table = Table()

    def pay(self, player, amount):
        """
        A player pays something
        player: player class of player who pays (type: player)
        amount: amount paid (type: int)
        return: None
        """
        player.update_balance(-amount)
        player.bet += amount
        player.total += amount
                    
    def pot_payments(self, payments, active):
        """
        Divide up the pot according to payment each round \n
        payments: amount paid by each person for a whole round (type: list) \n
        active: all active players by the end of the round (type: list) \n
        return: None
        """
        payments = sorted(payments)
        payments.insert(0, 0)

        for i, payment in enumerate(payments):
            for player in active:
                if player.bet >= payment:
                    try:
                        current_pot = self.pots[self.pots_i + i]
                    except IndexError:
                        self.pots.append(Pot())
                        current_pot = self.pots[self.pots_i + i]
                    current_pot.amount += (payment - payments[i - 1])
                    if player not in current_pot.assoc_ps:
                        current_pot.assoc_ps.append(player)

        payments.pop(0)
        self.pots_i += len(payments) - 1

    def start_round(self, first):
        """
        Initializes all the important variables in game \n
        first: is this the first round? (type: bool) \n
        blinds: [small blind, big blind] (type: tuple) \n
        return: all active players
        """
        # Generate cards
        nums = range(2, 15)
        nums = [num / 5 for num in nums]
        suits = ["diamonds", "hearts", "spades", "clubs"]

        for num in nums:
            for suit in suits:
                self.cards.append(Card(num, suit))

        # Important variables
        self.player_index = self.player_count - 1

        # Choose roles
        if first:
            self.dealer_i = randint(0, self.player_index) # Index of dealer
            self.small_blind_i = (self.dealer_i + 1) % self.player_count # Index of small blind
            self.big_blind_i = (self.dealer_i + 2) % self.player_count # Index of big blind
        else:
            # Move all roles down one
            self.dealer_i = (self.dealer_i + 1) % self.player_count
            self.small_blind_i = (self.small_blind_i + 1) % self.player_count
            self.big_blind_i = (self.big_blind_i + 1) % self.player_count

        # Set roles
        self.dealer = self.players[self.dealer_i]
        self.small_blind = self.players[self.small_blind_i]
        self.big_blind = self.players[self.big_blind_i]

        # Print roles
        print(f"{self.dealer.name} is the dealer")
        print(f"{self.small_blind.name} is the small blind")
        print(f"{self.big_blind.name} is the big blind")

        # Blinds pay
        self.pay(self.small_blind, self.blinds[0])
        self.pay(self.big_blind, self.blinds[1])

        player_list = [person for person in self.players if person.status]
        player_list = self.starter(player_list)

        # Give out cards
        for player in self.active:
            hand = player.get_cards(self.cards)
            self.cards = hand

        return player_list

    def check_bet(self, player):
        """
        Asks for user to check, bet, or fold.  Returns user input
        player: respective Player object who is up (type: Player)
        return: [amount paid, amount the ante is raised by] (type: list)
        """
        # Report player's current bet
        print(f"Your turn (${player.bet} bet so far)")

        while True: # Keep asking until answer is valid
            # Ask user input
            user_in = input("Check ($0), bet, or fold? ").lower()

            # Comprehend user input
            if user_in == "check":
                return [0, 0]
            elif user_in == "bet":
                while True: # Keep asking until answer is valid
                    try:
                        bet = int(input("How much do you want to bet? "))
                        # Check if player can pay
                        if bet <= player.balance:
                            return [bet, bet]
                        else:
                            print("Insufficient balance.")
                    except ValueError:
                        print("Input not understood")
            elif user_in == "fold":
                player.fold()
                return [0, 0]
            else:
                print("Input not understood.")

    def call_raise(self, player):
        """
        Asks for user to call, raise, or fold.  Returns user input
        player: respective Player object who is up (type: Player)
        ante: the current ante (type: int)
        return: [amount paid, amount the ante is raised by] (type: list)
        """
        # Report player's current bet
        print(f"Your turn (${player.bet} bet so far)")

        while True: # Keep asking until answer is valid
            # Ask user input
            user_in = input(f"Call (${self.ante - player.bet}), raise, or fold? ").lower()

            # Comprehend user input
            if user_in == "call":
                return [self.ante - player.bet, 0]
            elif user_in == "raise":
                while True:
                    try:
                        raise_in = int(input("How much do you want to raise by? "))
                        # Check if player can pay
                        if raise_in + self.ante <= player.balance:
                            return [raise_in + self.ante - player.bet, raise_in]
                        else:
                            print("Insufficient balance.")
                    except ValueError:
                        print("Input not understood.")
            elif user_in == "fold":
                player.fold()
                return [0, 0]
            else:
                print("Input not understood.")
        
    def all_in(self, player):
        """
        Asks for user to go all-in, or fold.  Returns user input
        player: respective Player object who is up (type: Player)
        return: amount paid (type: int)
        """
        # Report player's current bet
        print(f"Your turn (${player.bet} bet so far)")

        while True: # Keep asking until answer is valid
            # Ask user input
            user_in = input(f"Go all-in (${player.balance}) or fold? ").lower()
            
            # Comprehend user input
            if user_in == "all-in":
                player.all_in = True
                return [player.balance, 0]
            elif user_in == "fold":
                player.fold()
                return [0, 0]
            else:
                print("Input not understood.")

    def starter(self, active):
        """
        Determines the order of the players, based on the big blind
        active: All players still in the game (type: list)
        return: players rearranged with the player after the big blind first (type: list)
        """
        self.active = active

        # Decide the starter
        self.start_index = (self.big_blind_i + 1) % self.player_count
        self.active = self.active[self.start_index:] + self.active[:self.start_index] # Set the starter at the beginning of the active list
        self.players = self.active

        return self.active

    def run_betting(self, ante, active):
        """
        ante: ante (type: int)
        active: list of active players (type: list)
        return: {players who haven't folded, players who haven't paid the ante, the ante} (type: dict)
        """
        # Important variables
        self.active = active
        self.ante = ante

        # Run round of betting
        for person in self.active:
            # Check or bet
            if self.ante == person.bet:
                # Check if player is playable
                if person.playable == True:
                    res = self.check_bet(person)
                else:
                    res = person.non_playable_input("cb", 0)
            # All-in
            elif person.balance <= self.ante:
                # Check if player is playable
                if person.playable == True:
                    res = self.all_in(person)
                else:
                    res = person.non_playable_input("ai", 0)
            # Call or raise
            else:
                # Check if player is playable
                if person.playable == True:
                    res = self.call_raise(person)
                else:
                    res = person.non_playable_input("cr", self.ante)
            
            # Person pays the amount
            self.pay(person, res[0])
            self.ante += res[1]

            if person.balance == 0:
                person.all_in = True
            
            # Return if all have folded
            self.active = [person for person in self.players if person.status]
            self.all_in_ = [person for person in self.players if person.all_in]
            self.not_paid = [person for person in self.active if person.bet != self.ante]
            self.result = {"active": self.active, "not_paid": self.not_paid, "ante": self.ante, "all_in": self.all_in_}
    
            if len(self.active) == 1:
                return self.result

        return self.result
    
    def determine_winner(self, active):
        """
        Loop through each pot, determine the person with the highest hand value, award them the pot value
        active: list of active players (type: list)
        return: winner message to print (type: str)
        """
        # Remove placeholder pot
        self.pots.pop(0)

        # Loop through pots
        for i, pot in enumerate(self.pots):
            print(f"Pot #{i + 1}")
            eligible = [player for player in active if player in pot.assoc_ps]

            for player in eligible:
                # Get each players hand values
                player.get_hand_value(self.table.table)

                # Print the hand values
                print(f"{player.name} has {player.hand_name} (", end = "")
                for card in player.hand_cards[:-1]:
                    print(card, end = ", ")
                print(f"{player.hand_cards[-1]})")
            
            # Determine who had the best hand
            contenders = sorted(eligible, key = lambda player: player.hand_value)
            winner = contenders[-1]

            # Update balances
            pot_total = pot.amount
            winner.update_balance(pot_total)

            return f"{winner.name} wins ${pot_total}!"
    
    def fold_out(self, last_player):
        """
        Award all pots to last player standing during fold-out
        last_player: last player standing (type: Player)
        return: winner message to print (type: str)
        """
        # Remove placeholder pot
        self.pots.pop(0)

        winner = last_player
        pot_total = sum([pot.amount for pot in self.pots])

        return f"{winner.name} wins {pot_total}"

    def run_round(self):
        """
        Run a single round, 5 rounds of betting or until everyone has folded or went all-in
        return: all players who finished the round active (type: list)
        """
        active = self.start_round(True)
        all_in = list()

        # Keep playing rounds while the 5th street hasn't been shown / there are more than 1 players
        while self.round_num < 5 and len(self.active) > 1:
            print(f"\nRound #{self.round_num}")

            # Important variables
            if self.round_num == 1:
                ante = self.blinds[1]
            else:
                ante = 0
            self.round_num += 1
            not_paid = [person for person in active if person not in all_in]

            # Run betting

            while len(not_paid) > 0:

                # Run betting
                betting = self.run_betting(ante, not_paid)
                active = betting["active"]
                all_in = betting["all_in"]
                not_paid = betting["not_paid"]
                ante = betting["ante"]

                # Player who haven't folded / paid the ante
                not_paid = [person for person in active if person in not_paid]
                not_paid = [person for person in not_paid if person not in all_in]

            # Divide up the pot
            payments = list(set([person.bet for person in active]))
            self.pot_payments(payments, active)

            # Get the cards to table
            if self.round_num == 2:
                show = self.table.show_card(self.cards, 3)
                show_name = "flop"
            elif self.round_num == 3:
                show = self.table.show_card(self.cards, 1)
                show_name = "turn"
            elif self.round_num == 4:
                show = self.table.show_card(self.cards, 1)
                show_name = "river"

            # Print the cards
            if self.round_num < 5:
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
        
        return self.active
