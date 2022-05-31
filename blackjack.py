import random

playing = True


class Card:
    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return f'The deck has: {deck_comp}'

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
              'Jack': 10,
              'Queen': 10, 'King': 10, 'Ace': 11}

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += self.values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Place bet: '))
        except ValueError:
            print('Must be integer, Try Again!')
        else:
            if chips.bet > chips.total:
                print(f'Bet must be within {chips.total}')
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stick(deck, hand):
    global playing

    while True:

        x = input("\nWould you like to Hit or Stick? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("\nPlayer sticks. Dealer is playing.")
            playing = False

        else:
            print("Try again.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(chips):
    chips.lose_bet()
    print('\nPlayer Bust!')


def player_wins(chips):
    chips.win_bet()
    print('\nPlayer Wins!')


def dealer_busts(chips):
    chips.win_bet()
    print('\nDealer Bust!')


def dealer_wins(chips):
    chips.lose_bet()
    print('\nDealer Wins!')


def push():
    print("\nDealer and Player tie! It's a push.")


def main():
    global playing

    print('Welcome To Blackjack!\n')

    # initialises and shuffles players chips and a deck of cards
    game_deck = Deck()
    game_deck.shuffle()

    player_chips = Chips()

    while playing:

        player_hand = Hand()
        dealer_hand = Hand()

        hit(game_deck, player_hand)
        hit(game_deck, dealer_hand)
        hit(game_deck, player_hand)
        hit(game_deck, dealer_hand)

        print(f'Player Chips: {player_chips.total} \n')

        # Prompts the Player for their bet
        take_bet(player_chips)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        while playing:
            hit_or_stick(game_deck, player_hand)

            show_some(player_hand, dealer_hand)

            if player_hand.value > 21:
                player_busts(player_chips)
                break

        # If Player hasn't bust out, play Dealer's hand until Dealer reaches 17, then check for win conditions
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(game_deck, dealer_hand)

                # Show all cards
            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_chips)

            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_chips)

            elif player_hand.value > dealer_hand.value:
                player_wins(player_chips)

            else:
                push()

        # Inform Player of their winnings
        print(f'\nPlayer Chips: {player_chips.total}')
        # Ask to play again
        new_game = input("\nWould you like to play another hand? Enter 'y' or 'n' ")

        if new_game[0].lower() == 'y':
            playing = True
            print('\n' * 100)
            continue
        else:
            print("\nThanks for playing!")
            break


if __name__ == '__main__':
    main()
