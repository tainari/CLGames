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


game_boards = []
max_guess_dict = {1: 6, 2: 7, 4: 9, 8: 13}
num_board_dict = {'easy': 1, 'medium': 2, 'hard': 4, 'expert': 8}

def set_board_number():
    while True:
        ans = input("Do you want to play easy, medium, hard, or expert?\n")
        if ans in ['easy','medium','hard','expert']:
            return num_board_dict[ans]
        else:
            print("Not a valid option. Please try again.")

def new_game_board(n_boards=1,n_rows=6):
    game_board = [[[' - ', ' - ', ' - ', ' - ', ' - ']
                  for _ in range(n_rows)] for _ in range(n_boards)]
    return game_board

def print_game_board(game_boards,letters=[]):
    for n in range(max_guesses):
        row = []
        for board in game_boards:
            #print(board)
            #input("pause")
            row.append("  ".join(board[n]))
        print(" | ".join(row))
    # for row in game_board:
    #     print("  ".join(row))
    print()
    print(" ".join(letters))

def get_word_guess():
    while True:
        user_guess = input("Guess a five-letter word.\n").upper()
        if user_guess in valid_words:
            return list(user_guess)
        else:
            if len(user_guess) > 5:
                print("Word is too long. Guess again.")
            elif len(user_guess) < 5:
                print("Word is too short. Guess again.")
            else:
                print("Word is not valid. Try again.")

def check_word(guess,actual,words_won):
    results = []
    for n,codeword in enumerate(actual):
        if words_won[n]:
            result = ["++", "++", "++", "++", "++"]
            results.append(result)
        else:
            result = ["--", "--", "--", "--", "--"]
            remaining_letters = []
            #check first for right letter, right place
            for n, ch in enumerate(guess):
                if ch == codeword[n]:
                    result[n] = "++"
                #if not correct, add leftover codeword letters
                #to a separate array to check later
                else:
                    remaining_letters.append(codeword[n])
            #iterate over word again, checking for out-of-place
            #but correct letters; ensure no double-counting
            #by popping "remaining letters" 
            for n,ch in enumerate(guess):
                if result[n] != "++" and ch in remaining_letters:
                    result[n] = "+-"
                    remaining_letters.remove(ch)
            results.append(result)
    return results


colour_dict = {
    '++': '\x1b[6;30;42m ',
    '+-': '\x1b[6;30;43m ',
    '--': '\x1b[2;30;47m '
}
end_str = ' \x1b[0m'


def format_word(guess, results, words_won=[False, False, False, False, False]):
    formatted = []
    for n,result in enumerate(results):
        if words_won[n]:
            formatted.append(["   ","    ","   ","   ","   "])
        else:
            formatted.append([colour_dict[result[n]] + ch + end_str for n, ch in enumerate(guess)])
    return formatted


print(game_name)
print("Welcome to Dordle!")
print("""Your goal is to guess not one, but TWO 5-letter words...
      ...at the same time!""")
print("Input any five-letter word.")
print("For each board, you'll see:")
print("\tRight letter, right place: Green")
print("\tRight letter, wrong place: Yellow")
print("\tLetter not in word: Black ")
num_boards = set_board_number()
max_guesses = max_guess_dict[num_boards]
print(f"You have {max_guesses} guesses to guess {num_boards} words. Good luck!")
input("Enter anything to begin.\n")

play = True
while play:
    #clear screen for clean experience
    os.system('clear')
    # reset game board, reset values
    game_board = new_game_board(num_boards,max_guesses)
    words_won = [False for _ in range(num_boards)]
    #game_board_2 = refresh_game_board()
    num_guesses = 0
    win = False
    letters = ['A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    #choose a word
    secret_words = [choose_word(game_words) for _ in range(num_boards)]
    #start game!
    while not win and num_guesses < max_guesses:
        os.system('clear')
        print_game_board(game_board, letters)
        #get user input
        user_guess = get_word_guess()
        num_guesses += 1
        #check success of word
        result = check_word(user_guess,secret_words,words_won)
        #format word for printing
        formatted = format_word(user_guess,result,words_won)
        #print(formatted)
        for n,ch in enumerate(user_guess):
            if ch in letters:
                letters.remove(ch)
                #letters[letters.index(ch)] = formatted[n]
        #update which words have been won
        words_won = [True if r == ["++", "++", "++", "++","++"]\
                     else False\
                     for r in result]
        print(words_won)
        #update game board
        for n, board in enumerate(game_board):
            game_board[n][num_guesses-1] = formatted[n]
        if all(words_won):
            win = True
    os.system('clear')
    print_game_board(game_board)
    if win:
        print(f'You won in {num_guesses} guesses! Good job.')
    else:
        print('You lost! Sorry.')
        print(f'The correct guess was: {secret_words}')
    once_more = input(
        'Would you like to play again?\nType yes or no.\n').lower()
    if once_more == 'y' or once_more == 'yes':
        play = True
    else:
        os.system('clear')
        play = False