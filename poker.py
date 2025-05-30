import random
import os
import time

def clear():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux (os.name is 'posix')
    else:
        _ = os.system('clear')

clear()

print("Welcome to poker :D")

cards = {
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"
}

highest_cards = {}

suits = {
    "spades", "hearts", "diamonds", "clubs"
}

deck = [(card, suit) for card in cards for suit in suits]

player1 = {
    "name": None, 
    "player": 1, 
    "hand": [], 
    "money": 1000
}

player2 = {
    "name": None, 
    "player": 2, 
    "hand": [], 
    "money": 1000
}

player3 = {
    "name": None, 
    "player": 3, 
    "hand": [], 
    "money": 1000
}

player_test = {
    "name": None, 
    "player": 0, 
    "hand": [("9", "hearts"), ("7", "hearts"), ("2", "hearts"), ("7", "hearts"), ("10", "hearts"), ("6", "diamonds")], 
    "money": 1000
}
print(f"PLayertest: {player_test['hand']}")

def deal_cards(player):
    player["hand"] = random.sample(deck, 2)
    for card in player["hand"]:
        deck.remove(card)

def show_hand(player):
    print(f"Player {player['player']}'s cards showing in 4 seconds.")
    time.sleep(4)
    print(f"Player {player['player']}'s hand:")
    print(f"{player['hand'][0][0]} of {player['hand'][0][1]} and {player['hand'][1][0]} of {player['hand'][1][1]}")

def show_river():
    length = len(river)
    if length == 3:
        print("The flop shows a:", end=" ")
    elif length == 4:
        print("The turn shows a:", end=" ")
    else:
        print("The river shows a:", end=" ")
    for i in range(length):
        print(f"{river[i][0]} of {river[i][1]}", end=", ")
    print()



river_deck = [
    deck[random.randint(0, len(deck)-1)],
    deck[random.randint(0, len(deck)-1)]
]
river = [
    deck[random.randint(0, len(deck)-1)], 
    deck[random.randint(0, len(deck)-1)],
    deck[random.randint(0, len(deck)-1)]
]


# Hands ranking (lowest to highest):
# High card - highest card in hand
# One pair - a pair of cards with same number/letter
# Two pair - 2 pairs of cards with the same number/letter
# Three of a kind - 3 cards that have the same number/letter
# Straight - 5 cards in sequential order, ace can be used as 1 or 14
# Flush - 5 cards of the same suit, in any order
# Full house - a three of a kind plus a pair in the same hand
# Four of a kind - 4 cards of the same number or letter
# Straight flush - a flush, in sequential order
# Royal flush - highest hand in poker, straight flush but 10-A

suits = {"hearts", "spades", "diamonds", "clubs"}
royal_cards = {"10", "Jack", "Queen", "King", "Ace"}

def is_royal_flush(player):
    hand = player["hand"] + river
    suit_cards = {suit: [] for suit in suits}
    for card in hand:
        suit_cards[card[1]].append(card)
    for suit, cards in suit_cards.items():
        same_suit_royal_cards = [card for card in cards if card[0] in royal_cards]
        if len(same_suit_royal_cards) == 5:
            return True
    return False

def is_straight_flush(player):
    hand = player["hand"] + river
    suit_cards = {suit: [] for suit in suits}
    for card in hand:
        suit_cards[card[1]].append(card)
    for suit, cards in suit_cards.items():
        if len(cards) >= 5:
            card_values = []
            for card in cards:
                if card[0] == "Jack":
                    card_values.append(11)
                elif card[0] == "Queen":
                    card_values.append(12)
                elif card[0] == "King":
                    card_values.append(13)
                elif card[0] == "Ace":
                    card_values.append(14)
                    card_values.append(1)
                else:
                    card_values.append(int(card[0]))
            card_values = list(set(card_values))
            card_values.sort()
            for i in range(len(card_values) - 4):
                if card_values[i] + 4 == card_values[i + 4] and \
                   card_values[i + 1] == card_values[i] + 1 and \
                   card_values[i + 2] == card_values[i] + 2 and \
                   card_values[i + 3] == card_values[i] + 3:
                    return True
    return False

def is_four_of_a_kind(player):
    hand = player["hand"] + river
    ranks = {}
    for card in hand:
        rank = card[0]
        if rank in ranks:
            ranks[rank] += 1
        else:
            ranks[rank] = 1
    return any(count == 4 for count in ranks.values())

def is_full_house(player):
    hand = player["hand"] + river
    ranks = {}
    for card in hand:
        rank = card[0]
        if rank in ranks:
            ranks[rank] += 1  
        else:
            ranks[rank] = 1
    isthree = any(count == 3 for count in ranks.values())
    if isthree == True:
        ranks = {}
    for card in hand:
        rank = card[0]
        if rank in ranks:
            ranks[rank] += 1
        else:
            ranks[rank] = 1
    istwo = any(count == 2 for count in ranks.values())
    if istwo == True:
        return True
    else:
        return False
    
def is_flush(player):
    hand = player["hand"] + river
    suit_counts = {suit: 0 for suit in suits}
    for card in hand:
        suit_counts[card[1]] += 1
    return any(count >= 5 for count in suit_counts.values())

def is_straight(player):
    pre_hand = player["hand"] + river
    hand = []
    for card in pre_hand:
        if card[0] == "Jack":
            hand.append(11)
        elif card[0] == "Queen":
            hand.append(12)
        elif card[0] == "King":
            hand.append(13)
        elif card[0] == "Ace":
            hand.append(14)
            hand.append(1)
        else:
            hand.append(int(card[0]))
    
    hand = list(set(hand))
    hand.sort()
    for i in range(len(hand) - 4):
        if hand[i:i+5] == list(range(hand[i], hand[i] + 5)):
            return True
    return False

def is_three_of_a_kind(player):
    hand = player["hand"] + river
    ranks = {}
    for card in hand:
        rank = card[0]
        if rank in ranks:
            ranks[rank] += 1
        else:
            ranks[rank] = 1
    return any(count == 3 for count in ranks.values())

def is_two_pair(player):
    hand = player["hand"] + river
    ranks = {}
    for card in hand:
        rank = card[0]
        if rank in ranks:
            ranks[rank] += 1
        else:
            ranks[rank] = 1
    pair_count = sum(1 for count in ranks.values() if count == 2)
    return pair_count >= 2

def is_pair(player): 
    hand = player["hand"] + river
    ranks = {}
    for card in hand:
        rank = card[0]
        if rank in ranks:
            ranks[rank] += 1
        else:
            ranks[rank] = 1
    pair_count = sum(count == 2 for count in ranks.values())
    return pair_count == 1

def highest_card(player):
    hand = player["hand"] + river
    card_values = []
    for card in hand:
        if card[0] == "Jack":
            card_values.append(11)
        elif card[0] == "Queen":
            card_values.append(12)
        elif card[0] == "King":
            card_values.append(13)
        elif card[0] == "Ace":
            card_values.append(14)
        else:
            card_values.append(int(card[0]))
    return max(card_values)

def player_action(player, current_bet):
    print(f"{player['name']}, it's your turn!")
    print(f"Your current money: ${player['money']}")
    print(f"The current bet is: ${current_bet}")
    action = input("Choose an action (fold, call, raise): ").strip().lower()

    if action == "fold":
        print(f"{player['name']} folds.")
        return "fold", 0
    elif action == "call":
        if player["money"] >= current_bet:
            player["money"] -= current_bet
            print(f"{player['name']} calls and matches the bet of ${current_bet}.")
            return "call", current_bet
        else:
            print(f"{player['name']} does not have enough money to call. Automatically folding.")
            return "fold", 0
    elif action == "raise":
        raise_amount = int(input("Enter the amount to raise: "))
        total_bet = current_bet + raise_amount
        if player["money"] >= total_bet:
            player["money"] -= total_bet
            print(f"{player['name']} raises the bet to ${total_bet}.")
            return "raise", total_bet
        else:
            print(f"{player['name']} does not have enough money to raise. Automatically folding.")
            return "fold", 0
    else:
        print("Invalid action. Automatically folding.")
        return "fold", 0

def betting_round(players, current_bet):
    for player in players:
        if player["money"] > 0:
            action, bet = player_action(player, current_bet)
            if action == "fold":
                player["folded"] = True
            elif action == "raise":
                current_bet = bet
    return current_bet

# Game loop
def main():
    global river
    print("Welcome to poker :D")
    player1["name"] = input("Enter Player 1's name: ")
    player2["name"] = input("Enter Player 2's name: ")
    player3["name"] = input("Enter Player 3's name: ")

    players = [player1, player2, player3]
    for player in players:
        player["folded"] = False

    deal_cards(player1)
    deal_cards(player2)
    deal_cards(player3)

    show_hand(player1)
    show_hand(player2)
    show_hand(player3)

    river = random.sample(deck, 5)
    for card in river:
        deck.remove(card)

    current_bet = 0
    print("\n--- Pre-Flop Betting Round ---")
    current_bet = betting_round(players, current_bet)

    print("\n--- Flop ---")
    show_river()
    current_bet = betting_round(players, current_bet)

    print("\n--- Turn ---")
    show_river()
    current_bet = betting_round(players, current_bet)

    print("\n--- River ---")
    show_river()
    current_bet = betting_round(players, current_bet)

    print("\n--- Showdown ---")
    for player in players:
        if not player["folded"]:
            print(f"{player['name']}'s highest card: {highest_card(player)}")

if __name__ == "__main__":
    main()
