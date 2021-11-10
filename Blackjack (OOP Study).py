import random

#Firt we've got to set the card and the deck.
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}
        
class Card:

    def __init__(self, suit, rank):  
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    #Let's just add a __str__ to check if the cards are rigth.
    def __str__(self):
        return self.rank + ' of ' + self.suit

'''two_hearts = Card('Hearts', 'Two')
print(two_hearts)'''

class Deck:

    def __init__(self): #Create a deck and add all the 52 possible cards to it
        self.all_cards = []
        for suit in suits:
            for rank in ranks: 
                self.all_cards.append(Card(suit, rank))
    
    def shuffle(self): #Shuffle the deck 
        random.shuffle(self.all_cards)

    def deal(self): #Remove one card from the deck
        return self.all_cards.pop()

'''mydeck = Deck()
print(len(mydeck.all_cards))'''

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0 #as the Ace can have it's value changed from 1 to 11, we'll use this atribute to keep track of it
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 #keep track of how many aces we have


    def adjust_for_ace(self): 
        #Changes the Ace's value from 11 to 1 by subtracting 10 from the value if the total sum of the cards is greater than 21
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1 
'''
Just a little check to see if everything is working so far:
test_deck = Deck()
test_deck.shuffle()
test_player = Hand()
test_player.add_card(test_deck.deal())
test_player.add_card(test_deck.deal())
test_player.value
for card in test_player.cards:
    print(card)
'''

class Chips: #Class to keep track of 

    def __init__(self):
        self.total = 500 #default value, can be changed to whatever
        self.bet = 0  #will be change later on to the value the player determine during the game.
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips): #Function to ask the player how much he's going to bet
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, please insert an integer!')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you only have {chips.total} to bet')
            else:
                break

def hit(deck,hand): #if the player chooses to continue recieving cards
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

playing = True

def hit_or_stand(deck, hand):
    global playing #Variable we'll use during the while loop to check if the game continues.
    while True:
        x = input("Do you want to Hit or Stand? Answer with 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand) 
            #If the player decide to hit, we run the hit function to add a card to his hand and go back to the top of the while loop
        elif x[0].lower() == 's':
            print("The player Stands. Dealer's turn")
            playing = False
        else:
            print("Sorry, that's not a possible answer")
        break

def show_some(player, dealer): #Shows all the player's cards but hide one of the dealer's
    print ("\nDealer's hand:")
    print ('<Hidden Card>  ')
    print(dealer.cards[1])
    print("\n")
    print("Player's Cards:",*player.cards, sep = '\n')

def show_all(player,dealer): #Shows both hands
    print ("\nDealer's hand:")
    print(*dealer.cards, sep = '\n')
    print('\n')
    print("Player's cards: ",*player.cards, sep = '\n') 

#Now we'll write the functions that take care of the end game:

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

#Now, we'll create a while loop that runs the game itself.
while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')

    #Firts, let's create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    #Deals two card for each player:
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())


    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #Define the player's chips using the default value of 500, but it can be changed just by ading a argument to the method.
    player_chips = Chips()

    #Define the bet value:
    take_bet(player_chips)

    show_some(player_hand,dealer_hand) #Shows us the cards that start the game

    while playing: #Check if the player want to hit or stand:
        hit_or_stand(deck,player_hand)

        show_some(player_hand, dealer_hand) #shows the cards but hide one of the dealer's

        if player_hand.value > 21: #If the player busts:
            player_busts(player_hand, dealer_hand, player_chips)
            break
            
    if player_hand.value <= 21: #If the player do not bust:
        
        while dealer_hand.value < 17: #The dealer hits until he has 17 (Just a default value, can be changed as well)
            hit(deck,dealer_hand)    
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand) 

    # Inform Player of their chips total 
    print("\nPlayer's chips stand at: ",player_chips.total)
    
    # Ask if the player wants to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break