import random

#select set of 4 random colors
#duplicates are allowed, blanks are not
# RD = Red
# BU = Blue
# YW = Yellow
# GN = Green
# WH = White
# BK = Black

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

colors = ['r','b','y','g','w','k']
game_board = None

def create_code():
    return [colors[random.randint(0,len(colors)-1)] for _ in range(4)]

def refresh_game_board(n_rows = 12):
    game_board = [['-', '-', '-', '-', '|', '-', '-', '-', '-'] * n_rows]
    return game_board


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

print(game_name)
play = True
while play:
    all_guesses = []
    all_results = []
    game_board = refresh_game_board()
    num_guesses = 0
    max_guesses = 12
    win = False
    secret_code = create_code()
    print(secret_code)
    while not win and num_guesses < max_guesses:
        print(f'Guess number: {num_guesses}')
        bad_input = True
        user_guess = ""
        while bad_input:
            user_guess = list(input('Please provide a code sequence.\nAvailable colours: r, b, y, g, w, k\n').lower())
            input_test = [True if x in colors else False for x in user_guess]
            if all(input_test) and len(user_guess) == 4:
                bad_input = False
                num_guesses += 1
                all_guesses.append(user_guess)
            else:
                print("Input is not valid. Please try again.")
        results = check_guesses(user_guess, secret_code)
        all_results.append(results)
        print(f'Results: {results}')
        if results == ['r','r','r','r']:
            win = True
    if win:
        print(f'You won in {num_guesses} guesses! Good job.')
    else:
        print('You lost! Sorry.')
        print(f'The correct guess was: {secret_code}')
    once_more = input('Would you like to play again?\nType yes or no.\n').lower()
    if once_more == 'y' or once_more == 'yes':
        play = True
    else:
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
