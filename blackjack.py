import random

# Initialize deck of cards
suits = ["♤", "♧", "♢", "♡"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def calculate_hand_value(hand):
    value = 0
    num_aces = 0

    for rank, _ in hand:
        if rank in ("J", "Q", "K"):
            value += 10
        elif rank == "A":
            num_aces += 1
        else:
            value += int(rank)

    # Handle Aces (can be 1 or 11)
    for _ in range(num_aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1

    return value

def main():
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print(f"Player's hand: {player_hand[0][0]} of {player_hand[0][1]}, and {player_hand[1][0]} of {player_hand[1][1]}")
    print(f"Dealer's face-up card: {dealer_hand[0]}")

    while True:
        action = input("Do you want to hit or stand? ").lower()
        if action == "hit":
            player_hand.append(deal_card(deck))
            print(f"Player's hand: {player_hand[0][0]} of {player_hand[0][1]}, and {player_hand[1][0]} of {player_hand[1][1]}")
            if calculate_hand_value(player_hand) > 21:
                print("Bust! You lose.")
                break
        elif action == "stand":
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deal_card(deck))
            print(f"Dealer's hand: {dealer_hand}")
            player_value = calculate_hand_value(player_hand)
            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value > 21 or player_value > dealer_value:
                print("You win!")
            else:
                print("Dealer wins.")
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

if __name__ == "__main__":
    main()
