from random import sample, uniform, randrange
from itertools import combinations

class Player:
    def __init__(self, name):
        """
        Initialize a player with a balance of $10,000
        """
        self.name = name
        self.status = True
        self.all_in = False
        self.balance = 10000
        self.bet = 0
        self.total = 0
        if self.name == "Larry":
            self.playable = True
        else:
            self.playable = False

    def get_cards(self, temp_cards):
        """
        Picks out a hand from temp_cards
        temp_cards: All cards that are still available to be held (type: list)
        Return: None
        """
        # Pick out the cards
        card1, card2 = sample(temp_cards, 2)
        self.hand = [card1, card2]
        
        # Players cannot have the same card
        temp_cards.remove(card1)
        temp_cards.remove(card2)

        return temp_cards

    def face_translation(self, n):
        """
        Translates n to face value
        n: card face
        return: name of face, i.e. jack, queen, etc.
        """
        # Write name
        if n == 2.2:
            face_name = "jack"
        elif n == 2.4:
            face_name = "queen"
        elif n == 2.6:
            face_name = "king"
        elif n == 2.8:
            face_name = "ace"
        else:
            face_name = int(n * 5)
        
        return face_name

    def rep_counter(self, obj, n):
        """
        Finds objects that repeat
        obj: iterative object
        n: how many times object repeats
        return: object that repeats n times in obj
        """
        counter = list()

        for item in set(obj):
            if obj.count(item) == n:
                counter.append(item)
        
        return counter

    def get_hand_value(self, table):
        """
        Get value of hand
        table: five cards on table
        return: [numerical value of hand, name of hand, the five cards that constitute it]
        """
        self.cards = table + self.hand

        # All combinations of 5 cards
        combos = list(combinations(self.cards, 5))
        values = dict()

        # Evaluate each hand
        for combo in combos:
            # Important variables
            combo_nums = [card.face for card in combo]
            combo_suits = [card.suit for card in combo]

            # Write tie-breaking sums
            high_card = max(combo_nums)
            nums_descending = combo_nums
            nums_descending.sort(reverse = True)
            tie_break = [10**(-1 * i) * num for i, num in enumerate(nums_descending)]
            tie_break = sum(tie_break)

            # Get repetition of certain numbers
            rep_count = [combo_nums.count(num) for num in set(combo_nums)]
            straight_nums = [int(num * 5) for num in combo_nums]
            order = range(min(straight_nums), max(straight_nums))

            # Hands
            straight = sorted(combo_nums) == list(order)
            flush = len(set(combo_suits)) == 1
            four_of_a_kind = 4 in rep_count
            full_house = 3 in rep_count and 2 in rep_count
            three_of_a_kind = 3 in rep_count
            two_pair = rep_count.count(2) == 2
            pair = 2 in rep_count

            # Hand value
            if straight and flush:
                values[8000 + tie_break] = [combo, "a straight-flush"]
            
            elif four_of_a_kind:
                # Set tie breaker
                four_count = self.rep_counter(combo_nums, 4)[0]
                tie_break += four_count * 10
                values[7000 + tie_break] = [combo, "a four-of-a-kind"]
            
            elif full_house:
                three_count = self.rep_counter(combo_nums, 3)[0]
                two_count = self.rep_counter(combo_nums, 2)[0]
                tie_break += three_count * 100 + two_count * 10
                values[6000 + tie_break] = [combo, "a full-house"]
            
            elif flush:
                values[5000 + tie_break] = [combo, "a flush"]

            elif straight:
                values[4000 + tie_break] = [combo, "a straight"]

            elif three_of_a_kind:
                three_count = self.rep_counter(combo_nums, 3)[0]
                tie_break += three_count * 10
                values[3000 + tie_break] = [combo, "a three-of-a-kind"]

            elif two_pair:
                two_count = self.rep_counter(combo_nums, 2)
                two_count_l = max(two_count)
                two_count_s = min(two_count)
                tie_break += two_count_l * 100 + two_count_s * 10
                values[2000 + tie_break] = [combo, "two-pair"]

            elif pair:
                two_count = self.rep_counter(combo_nums, 2)[0]
                tie_break += two_count * 10
                pair_value = self.face_translation(two_count)
                values[1000 + tie_break] = [combo, f"a pair of {pair_value}s"]

            else:
                values[tie_break] = [combo, f"{self.face_translation(high_card)} high"]
        
        # Determine the best combo
        top_hand_key = max(values.keys())
        top_combo = values[top_hand_key]
        top_combo_cards = top_combo[0]
        top_combo_name = top_combo[1]

        top_combo = [card.name for card in top_combo_cards]

        self.hand_value = top_hand_key
        self.hand_name = top_combo_name
        self.hand_cards = top_combo

    def zero_bets(self):
        """
        Zero out bet
        """
        self.bet = 0

    def update_balance(self, amount):
        """
        Have player gain or lose some amount of money
        amount: amount to change balance by, positive for gain, negative for loss (type: int or float)
        Return: None
        """
        self.balance += amount

    def fold(self):
        """
        Player may fold, sets them to inactive and deletes their hand
        Return: None
        """
        self.status = False
        self.all_in = False
        self.hand = []

    def non_playable_input(self, intype, ante):
        """
        Returns simulated responses to check-bet, call-raise, and all-in inputs
        intype: type of input required (cb, cr, ai)
        return: proper response (list/int)
        """
        self.seed = uniform(0, 1)

        # If response is check or bet
        if intype == "cb":
            # 70% chance of check
            if self.seed < 0.7:
                print(f"{self.name} checked")
                return [0, 0]
            # 20% chance of bet
            elif self.seed < 0.9:
                self.bet_amount = randrange(10) * 100
                print(f"{self.name} bet ${self.bet_amount}")
                return [self.bet_amount, self.bet_amount]
            # 10% chance of fold
            else:
                self.fold()
                print(f"{self.name} folded")
                return [0,0]

        # If response is call or raise
        elif intype == "cr":
            # 70% chance of call
            if self.seed < 0.7:
                print(f"{self.name} called")
                return [ante - self.bet, 0]
            # 20% chance of raise
            elif self.seed < 0.9:
                self.raise_amount = randrange(10) * 100
                print(f"{self.name} raised by {self.raise_amount}")
                return [self.raise_amount, self.raise_amount]
            # 10% chance of fold
            else:
                self.fold()
                print(f"{self.name} folded")
                return[0, 0]
        
        else:
            # 70% chance of fold
            if self.seed < 0.7:
                self.fold()
                print(f"{self.name} folded")
                return [0, 0]
            else:
                print(f"{self.name} went all-in!")
                return [self.balance, 0]
