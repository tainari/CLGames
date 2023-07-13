#version of Wordle with TWO games that you play at the same time
# inspiration from https://dordle.io/
# Wordle: 6 guesses
# Dordle: 7 guesses
# Quordle: 9 guesses

# dictionaries knicked with gratitude from https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d

from random import choice as choose_word
import os

game_name = """
 ______   _______  ______    ______   ___      _______ 
|      | |       ||    _ |  |      | |   |    |       |
|  _    ||   _   ||   | ||  |  _    ||   |    |    ___|
| | |   ||  | |  ||   |_||_ | | |   ||   |    |   |___ 
| |_|   ||  |_|  ||    __  || |_|   ||   |___ |    ___|
|       ||       ||   |  | ||       ||       ||   |___ 
|______| |_______||___|  |_||______| |_______||_______|
"""

#Make a set so that searching if a word is valid is O(1)
valid_words = set()
with open('./nordle/wordle-Ta.txt','r') as f:
    for r in f:
        valid_words.add(r.strip().upper())

#Game words are a list in order to leverage random.choice
game_words = []
with open('./nordle/wordle-La.txt', 'r') as f:
    for r in f:
        game_words.append(r.strip().upper())
        valid_words.add(r.strip().upper())

game_board_1 = None
#game_board_2 = None
max_guesses = 6

def new_game_board(n_rows=6):
    game_board = [[' - ', ' - ', ' - ', ' - ', ' - ']
                  for _ in range(n_rows)]
    return game_board

def print_game_board(game_board):
    for row in game_board:
        print("  ".join(row))

def check_word(guess,actual):
    result = ["--", "--", "--", "--", "--"]
    remaining_letters = []
    #check first for right letter, right place
    for n, ch in enumerate(guess):
        if ch == actual[n]:
            result[n] = "++"
        #if not correct, add leftover codeword letters
        #to a separate array to check later
        else:
            remaining_letters.append(actual[n])
    #iterate over word again, checking for out-of-place
    #but correct letters; ensure no double-counting
    #by popping "remaining letters" 
    for n,ch in enumerate(guess):
        if result[n] != "++" and ch in remaining_letters:
            result[n] = "+-"
            remaining_letters.pop(remaining_letters.index(ch))
    return result


colour_dict = {
    '++': '\x1b[6;30;42m ',
    '+-': '\x1b[6;30;43m ',
    '--': '\x1b[1;37;40m '
}
end_str = ' \x1b[0m'

def format_word(guess,results):
    formatted = []
    return [colour_dict[results[n]] + ch + end_str \
            for n, ch in enumerate(guess)]


print(game_name)
print("Welcome to Dordle!")
print("""Your goal is to guess not one, but TWO 5-letter words...
      ...at the same time!""")
print("Input any five-letter word.")
print("For each board, you'll see:")
print("\tRight letter, right place: Green")
print("\tRight letter, wrong place: Yellow")
print("\tLetter not in word: Black ")
print("You have X guesses. Good luck!")
input("Enter anything to begin.\n")

play = True
while play:
    #clear screen for clean experience
    os.system('clear')
    # reset game board, reset values
    game_board_1 = new_game_board()
    #game_board_2 = refresh_game_board()
    num_guesses = 0
    win = False
    letters = ['A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    #choose a word
    secret_word = choose_word(game_words)
    #start game!
    while not win and num_guesses < max_guesses:
        os.system('clear')
        print_game_board(game_board_1)
        #get user input
        user_guess = ""
        bad_input = True
        while bad_input:
            user_guess = input("Guess a five-letter word.\n").upper()
            if user_guess in valid_words:
                bad_input = False
                num_guesses += 1
                user_guess = list(user_guess)
            else:
                if len(user_guess) > 5:
                    print("Wsord is too long. Guess again.")
                elif len(user_guess) < 5:
                    print("Word is too short. Guess again.")
                else:
                    print("Word is not valid. Try again.")
        #check success of word
        result = check_word(user_guess,secret_word)
        print("Result: ",result)
        #format word for printing
        formatted = format_word(user_guess,result)
        print("Format: ",formatted)
        #update game board
        game_board_1[num_guesses-1] = formatted
        if all([a=='++' for a in result]):
            win = True
    os.system('clear')
    print_game_board(game_board_1)
    if win:
        print(f'You won in {num_guesses} guesses! Good job.')
    else:
        print('You lost! Sorry.')
        print(f'The correct guess was: {secret_word}')
    once_more = input(
        'Would you like to play again?\nType yes or no.\n').lower()
    if once_more == 'y' or once_more == 'yes':
        play = True
    else:
        os.system('clear')
        play = False