from random import randint, choice

class Game:
    def __init__(self, players, cards):
        """
        Create a game \n
        players: list of players, of type player class (type: list) \n
        cards: list of all playable cards
        """
        self.players = players
        self.player_count = len(players)
        self.cards = cards
        self.round_num = 1

    def pay(self, player, amount):
        """
        A player pays something
        player: player class of player who pays (type: player)
        amount: amount paid (type: int)
        return: None
        """
        player.update_balance(-amount)
        player.bet += amount
        self.pot += amount

    def show_card(self, temp_cards, n):
        choices = list()

        for num in range(n):
            c = choice(temp_cards)
            choices.append(c)
            temp_cards.remove(c)
        
        self.cards = temp_cards
        return [choices, temp_cards]

    def start_round(self, first, blinds):
        """
        Initializes all the important variables in game \n
        first: is this the first round? (type: bool) \n
        blinds: [small blind, big blind] (type: tuple) \n
        return: all active players
        """
        # Important variables
        self.pot = 0
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
        self.pay(self.small_blind, blinds[0])
        self.pay(self.big_blind, blinds[1])

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
        return: integer containing the amount paid (type: int)
        """
        # Report player's current bet
        print(f"{player.name}'s turn (${player.bet} bet so far)")

        while True: # Keep asking until answer is valid
            # Ask user input
            user_in = input("Check ($0), bet, or fold? ").lower()

            # Comprehend user input
            if user_in == "check":
                return 0
            elif user_in == "bet":
                while True: # Keep asking until answer is valid
                    try:
                        bet = int(input("How much do you want to bet? "))
                        return bet
                    except ValueError:
                        print("Input not understood")
            elif user_in == "fold":
                player.fold()
                return 0
            else:
                print("Input not understood.")

    def call_raise(self, player, ante):
        """
        Asks for user to call, raise, or fold.  Returns user input
        player: respective Player object who is up (type: Player)
        ante: the current ante (type: int)
        return: [amount paid, amount the ante is raised by] (type: list)
        """
        # Report player's current bet
        print(f"{player.name}'s turn (${player.bet} bet so far)")

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
                        return [raise_in + self.ante - player.bet, raise_in]
                    except ValueError:
                        print("Input not understood.")
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
        self.round_num += 1

        # Run round of betting
        for person in self.active:
            if self.ante == person.bet: # Check or bet if the person has already paid the ante
                res = self.check_bet(person)
                self.pay(person, res)
                self.ante += res
            else: # Call or raise if player hasn't paid the ante
                res = self.call_raise(person, self.ante)
                self.pay(person, res[0]) # Person pays the amount
                self.ante += res[1]
            
            # Return if all have folded
            self.active = [person for person in self.active if person.status] 
            self.not_paid = [person for person in self.active if person.bet != self.ante]
            self.result = {"active": self.active, "not_paid": self.not_paid, "ante": self.ante}

            if len(self.active) == 1:
                return self.result

        return self.result
