import random
import os

game_name = """
 __   __  _______  _______  _______  _______  ______    __   __  ___   __    _  ______  
|  |_|  ||   _   ||       ||       ||       ||    _ |  |  |_|  ||   | |  |  | ||      | 
|       ||  |_|  ||  _____||_     _||    ___||   | ||  |       ||   | |   |_| ||  _    |
|       ||       || |_____   |   |  |   |___ |   |_||_ |       ||   | |       || | |   |
|       ||       ||_____  |  |   |  |    ___||    __  ||       ||   | |  _    || |_|   |
| ||_|| ||   _   | _____| |  |   |  |   |___ |   |  | || ||_|| ||   | | | |   ||       |
|_|   |_||__| |__||_______|  |___|  |_______||___|  |_||_|   |_||___| |_|  |__||______| 
"""
# name generated using https://patorjk.com/software/taag/#p=display&f=Modular&t=Mastermind

colours = ['r','b','y','g','w','k']
# reference for colour codes: 
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal/3332860#3332860
colour_dict = {'r': '\x1b[1;3;41m r \x1b[0m',
               'b': '\x1b[1;37;44m b \x1b[0m',
               'y': '\x1b[6;30;43m y \x1b[0m',
               'g': '\x1b[6;30;42m g \x1b[0m',
               'w': '\x1b[6;30;47m w \x1b[0m',
               'k': '\x1b[1;37;40m k \x1b[0m',
               "|": "\x1b[0m | ", 
               "-": "\x1b[0m - "}
game_board = None
max_guesses = 12
max_guess_dict = {'easy':12,'medium':10,'hard':8,'expert':6}

def create_code():
    # RD = Red
    # BU = Blue
    # YW = Yellow
    # GN = Green
    # WH = White
    # BK = Black
    # select set of 4 random colors
    # duplicates are allowed, blanks are not
    return [colours[random.randint(0,len(colours)-1)] for _ in range(4)]

def refresh_game_board(n_rows = 12):
    game_board = [['-', '-', '-', '-', '|', '-', '-', '-', '-'] for _ in range(n_rows)]
    return game_board

def print_game_board():
    print(
        "  \x1b[6;30;47m-----Guesses-----\x1b[0m    |   \x1b[6;30;47m-----Results-----\x1b[0m")
    print("                       |  ")
    for row in game_board:
        print("  "+"  ".join([colour_dict[x] for x in row]))
    return


def check_guesses(guess_array,code_array):
    result = []
    incorrect_guesses = []
    remaining_code = []
    #correct colour in correct place
    for n, g in enumerate(guess_array):
        if g == code_array[n]:
            result.append('r')
        else:
            remaining_code.append(code_array[n])
            incorrect_guesses.append(g)
    #incorrect colour in incorrect place:
    for g in incorrect_guesses:
        if g in remaining_code:
            result.append('w')
            remaining_code.pop(remaining_code.index(g))
    #return result :) 
    return result

##START GAME HERE
os.system('clear')
print(game_name)
print("Welcome to Mastermind!")
print("In this game, the computer will generate a secret code\
      of four colours (red, blue, yellow, green, white, black).")
print("Your goal is to guess the exact code.")
print("Each round, you will be able to guess a sequence of four colours.")
print("Repeats are allowed, but blanks are not.")
print("The computer will return how close your guess is:")
print("\tRed = you have the right colour in the right spot.")
print("\tWhite = you have the right colour in the wrong place.")
print("These results are *not* in order!")
bad_input = True
while bad_input:
    mode = input("Would you like to play in easy, medium, hard, or expert mode?\n")
    if mode in max_guess_dict:
        max_guesses = max_guess_dict[mode]
        bad_input = False
    else:
        print("Bad response. Please try again.")

play = True
while play:
    os.system('clear')
    all_guesses = []
    all_results = []
    game_board = refresh_game_board(max_guesses)
    num_guesses = 0
    win = False
    secret_code = create_code()
    #print(secret_code)
    while not win and num_guesses < max_guesses:
        print_game_board()
        print(f'Guess number: {num_guesses}')
        bad_input = True
        user_guess = ""
        while bad_input:
            user_guess = list(input('Please provide a code sequence.\nAvailable colours: r, b, y, g, w, k\n').lower())
            input_test = [True if x in colours else False for x in user_guess]
            if all(input_test) and len(user_guess) == 4:
                bad_input = False
                num_guesses += 1
                all_guesses.append(user_guess)
            else:
                print("Input is not valid. Please try again.")
        os.system('clear')
        results = check_guesses(user_guess, secret_code)
        all_results.append(results)
        game_board[num_guesses-1] = user_guess + ["|"] + results
        #print(f'Results: {results}')
        if results == ['r','r','r','r']:
            win = True
    os.system('clear')
    print_game_board()
    if win:
        print(f'You won in {num_guesses} guesses! Good job.')
    else:
        print('You lost! Sorry.')
        print(f'The correct guess was: {secret_code}')
    once_more = input('Would you like to play again?\nType yes or no.\n').lower()
    if once_more == 'y' or once_more == 'yes':
        play = True
    else:
        os.system('clear')
        play = False

#HOW TO PLAY THE GAME
#computer selects set of 4 random colors
#user guesses 
#computer provides feedback
#computer prints guesses and results to terminal 
#if same as key, user wins
#if number of guesses < max, go back to user guess
#if number of guesses = max, computer wins and game ends
#computer asks if play again


#12 rows of guesses (next level: easy(12), medium (10), hard (8), expert (6))
#white is wrong place, right colour
#red is right place, right colour

