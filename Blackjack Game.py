import random

class Card:
    def __init__(self, suit, rank, value):
        self.suit=suit
        self.rank=rank
        self.value=value 

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    suits = ["spades", "hearts", "clubs", "diamonds"]
    ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, 
          "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "Ace": 11}
    def __init__(self):
        self.cards=[Card(suit, rank, value) for suit in self.suits for rank, value in self.ranks.items()]

    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        if not self.cards:
            print("reshuffling the deck...")
            self.__init__()
            self.shuffle()
        return self.cards.pop()
class Hand:
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0
    def add_card(self, card):
        self.cards.append(card)
        self.value+=card.value 
        if card.rank =="Ace":
            self.aces += 1
        self.adjust_ace_value()
    def adjust_ace_value(self):
        while  self.value > 21 and self.aces: # self.aces == True
            self.value -= 10
            self.aces -= 1
class Player:
    def __init__(self, name):
        self.name=name
        self.hand=Hand()

    def hit(self, deck):
        self.hand.add_card(deck.deal())

    def is_busted(self):
        return self.hand.value > 21
    
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        
    def play(self, deck):
        while self.hand.value < 17:
            print("dealer hits...")
            self.hit(deck)
            print(f"dealer's new card: {self.hand.cards[-1]} (value: {self.hand.value})")

class Play_game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("player")
        self.dealer = Dealer()

    def deal_initial_cards(self):

        self.player.hit(self.deck)
        self.player.hit(self.deck)
        self.dealer.hit(self.deck)
        self.dealer.hit(self.deck)

        if self.player.hand.value == 21:
            print("Blackjack! You win!")
            return True
        return False

    def player_turn(self):
        while True:
            print(f"your card is:{[str(card) for card in self.player.hand.cards]} (value :{self.player.hand.value})") 
            if self.player.is_busted():
                print(f"you busted, dealer wins")
                return False
            action=input("do you want to hit or stand choose (h/s): ").lower().strip()
            if action not in ["h", "s", "hit", "stand"]:
                print("invalid input, please enter 'h' to hit or 's' to stand")
                continue
            if action == "h" or action == "hit":
                self.player.hit(self.deck)
            else:
                break
        return True
    def dealer_turn(self):
        print(f"dealer cards:hidden, {[self.dealer.hand.cards[1]]}")
        self.dealer.play(self.deck)
        
    def check_winner(self):
        print(f"your final hand: {[str(card) for card in self.player.hand.cards]} (value: {self.player.hand.value})")
        print(f"dealer's final hand: {[str(card) for card in self.dealer.hand.cards]} (value: {self.dealer.hand.value})")
        if self.player.is_busted():
            print("you busted, dealer wins")
        if self.dealer.is_busted():
            print("dealer busted, you win")
        elif self.player.hand.value > self.dealer.hand.value:
            print("you win")
        elif self.player.hand.value < self.dealer.hand.value:
            print("dealer wins")
        else:
            print("it's a tie")

    def start_game(self):
        while True:
            self.deck=Deck()
            self.deck.shuffle()
            self.player.hand=Hand()
            self.dealer.hand=Hand()

            print("---welcome to the game---")
            if self.deal_initial_cards():
                play_again = input("would you like to play again? (y/n)").lower().strip()
                if play_again != "y" and play_again != "yes":
                    print("thanks for playing")
                    break
                else:
                    continue
            print(f"dealer's cards: 1st is hidden, {self.dealer.hand.cards[1]} ")
            if self.player_turn():
                self.dealer_turn()
                self.check_winner()
            play_again = input("would you like to play again? (y/n)").lower().strip()
            if play_again != "y" and play_again!="yes":
                print("thanks for playing")
                break

if __name__=="__main__":
    game=Play_game()
    game.start_game()