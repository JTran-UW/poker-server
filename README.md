# poker-server
## server side of poker project

Opens up game of Texas hold-em poker, plays one round.

### Objects:
**Card**    
Attributes:  
 - face: card face value (i.e. 2, 3, 4, 5, etc.)
 - suit: card suit value (Spade, Hearts, etc.)
 - face_name: card face value name (11 = Jack, 12 = Queen, etc.)
 - name: name of card in full, in form face_name + of suit (Jack of Diamonds)

**Table**  
Attributes:  
 - table: all cards put on table (flop, river, etc.)  
Methods:    
 - show_card(temp_cards, n)  
    puts n cards on table out of temp_cards

**Pot**  
Attributes:  
 - amount: amount of money in pot
 - assoc_ps: players who have paid enough to be eligble for pot

**Player**  
Attributes:  
 - name: name of player
 - status: active status of player (boolean)
 - all_in: all-in status of player (boolean)
 - balance: amount of money player has
 - bet: amount of money player has bet during a single round of betting
 - total: total amount of money player has bet during full round
 - playable: status of player as playable or non-playable  
Methods:  
 - get_cards(temp_cards)  
    Picks out a hand (2 cards) from temp_cards
 - face_translation(n)  
    translates a face value of n to its face name (i.e. 11 to Jack)
 - rep_counter(obj, n)  
    searches for object in interative obj that repeats n times
 - hand_value(table)  
    gathers value of hand given the five cards on the table
 - zero_bets()  
    zeros out player bet
 - update_balance(amount)  
    updates player balance by some amount
 - fold()  
    updates player status to false
 - non_playable_input(intype, ante)  
    simulates user input, looking for input type intype, given the ante

**Game**  
Attributes:  
 - players: all players in game
 - player_count: number of players in game
 - cards: all 52 cards in card objects
 - round_num: the round number
 - pots: list of pots in pot objects
 - pots_i: the index of the current pot
 - blinds: blinds in tuple form, (small blind, big blind)  
Methods:  
 - pay(player, amount)  
    charge some player some amount
 - start_round(first, blinds)  
    initialize a round of betting, given some blinds, and a bool checking if this is the first round
 - check_bet(player)  
    get input from player given check or bet or fold options
 - call_raise(player, ante)  
    get input from player given call or raise or fold options
 - all_in(player)  
    get input from player given all-in or fold options
 - starter(active)  
    rearrange active list object to put the player after the big blind first
 - run_betting(ante, active)  
    run a round of betting for active players given the ante
 - pot_payments(payments, active)  
    takes payments from a round of betting of active players and divides them up into the proper pot.

