# This is a text-based version of the Tic Tac Toe game.
# https://www.google.com/search?q=tic+tac+toe

import random

line1 = ['1','|','2','|','3']
line2 = ['4','|','5','|','6']
line3 = ['7','|','8','|','9']
separate_line = "___________"
user_label = 'X'
computer_label = 'O'

available_selection = [1,2,3,4,5,6,7,8,9]
user_positions = []
computer_positions = []

winning_combo_positions = [
        # Horizontal Winning Positions
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        # Vertical Winning Positions
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        # Diagonal Winning Positions
        [0, 4, 8],
        [2, 4, 6],
    ]

continue_game = True
somebody_win = False

def board():
    [print(i, end=' ') for i in line1]
    print()
    print(separate_line)
    [print(i, end=' ') for i in line2]
    print()
    print(separate_line)
    [print(i, end=' ') for i in line3]
    print()

def user_input():
    global continue_game
    try:
        select_postion = int(input("\nInput the number of the position you would like to select:\n"))

        if select_postion in available_selection:
            available_selection.remove(select_postion)
            user_positions.append(select_postion-1)
            if select_postion == 1 or select_postion == 2 or select_postion == 3:
                line1[(select_postion-1)*2] = user_label
            elif select_postion == 4 or select_postion == 5 or select_postion == 6:
                line2[(select_postion-4)*2] = user_label
            elif select_postion == 7 or select_postion == 8 or select_postion == 9:
                line3[(select_postion-7)*2] = user_label

            else:
                print()
                print('Invalid input.')
                print()
        else:
            print()
            print('Invalid input.')
            print()

    except ValueError:
        print()
        print('Invalid input.')
        print()


def computer_input():
    comupter_select = random.choice(available_selection)

    if comupter_select in available_selection:
        available_selection.remove(comupter_select)
        computer_positions.append(comupter_select-1)
        if comupter_select == 1 or comupter_select == 2 or comupter_select == 3:
            line1[(comupter_select - 1) * 2] = computer_label
        elif comupter_select == 4 or comupter_select == 5 or comupter_select == 6:
            line2[(comupter_select - 4) * 2] = computer_label
        elif comupter_select == 7 or comupter_select == 8 or comupter_select == 9:
            line3[(comupter_select - 7) * 2] = computer_label

def if_win():
    global continue_game, somebody_win
    user_positions_set = set(user_positions)
    computer_positions_set = set(computer_positions)

    if somebody_win:  # Prevent rechecking after a win
        return

    for combo in winning_combo_positions:
        if user_positions_set >= set(combo):
            board()
            print('\nHooray! You win!')
            continue_game = False
            somebody_win = True

        elif computer_positions_set >= set(combo):
            board()
            print('\nFailed! Computer wins:(')
            continue_game = False
            somebody_win = True

    if not available_selection and not somebody_win:
        board()
        print('\nDraw!')
        continue_game = False
        somebody_win = True


while continue_game:
    board()
    user_input()
    if_win()
    if not continue_game:
        break
    computer_input()
    if_win()




