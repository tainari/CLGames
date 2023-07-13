import random

game_name = """
 _______  ___      _______  _______  ___   _      ___  _______  _______  ___   _ 
|  _    ||   |    |   _   ||       ||   | | |    |   ||   _   ||       ||   | | |
| |_|   ||   |    |  |_|  ||       ||   |_| |    |   ||  |_|  ||       ||   |_| |
|       ||   |    |       ||       ||      _|    |   ||       ||       ||      _|
|  _   | |   |___ |       ||      _||     |_  ___|   ||       ||      _||     |_ 
| |_|   ||       ||   _   ||     |_ |    _  ||       ||   _   ||     |_ |    _  |
|_______||_______||__| |__||_______||___| |_||_______||__| |__||_______||___| |_|
"""

point_dict = {
    "2":2,
    "3":3,
    "4":4,
    "5":5,
    "6":6,
    "7":7,
    "8":8,
    "9":9,
    "10":10,
    "J":10,
    "Q":10,
    "K":10,
    "A":11
}

def create_deck(num_decks = 6):
    suits = ["H","S","C","D"]
    vals = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    cards = []
    for n in range(num_decks):
        for s in suits:
            cards.extend([a+s for a in vals])
    return cards

def shuffle_deck(deck):
    return random.shuffle(deck)
deck = create_deck()
deck = shuffle_deck(deck)

play = True
while play:
    