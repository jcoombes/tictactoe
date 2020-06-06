"""
The quickest and dirtiest approach which can get a two player version of tic tac toe running in the terminal.
Inspired by Jakediederich's Pycon 2012 Talk "Stop Writing Classes"
"""

import numpy as np
import random
import copy
import time

def show_board(board: np.ndarray) -> str:
    zeroth_line = "\n"
    first_line = " {} | {} | {} ".format(board[0, 0], board[0, 1], board[0, 2])
    line_of_dashes = "--- --- ---"
    second_line = " {} | {} | {} ".format(board[1, 0], board[1, 1], board[1, 2])
    third_line = " {} | {} | {} ".format(board[2, 0], board[2, 1], board[2, 2])

    return "\n".join((zeroth_line, first_line, line_of_dashes, second_line, line_of_dashes, third_line, zeroth_line))


def turn_flipper(x_or_o: str) -> str:
    if x_or_o == 'x':
        return 'o'
    elif x_or_o == 'o':
        return 'x'
    else:
        raise ValueError(x_or_o + 'is neither "x" nor "o"')


def human_turn(board: np.ndarray, x_or_o: str) -> np.ndarray:
    """
    Careful, this also mutates data.
    :param board: numpy array containing game state.
    :param x_or_o: the string 'x' or the string 'o', whose side are they on.
    :return: board after move.
    """
    input2rowcol = {'e': (0, 0), 'r': (0, 1), 't': (0, 2),
                    'd': (1, 0), 'f': (1, 1), 'g': (1, 2),
                    'c': (2, 0), 'v': (2, 1), 'b': (2, 2)}

    user_input = ""

    while user_input not in input2rowcol.keys():
        user_input = input("Use your keyboard to select your location, player " + x_or_o + ": ")

    board[input2rowcol[user_input]] = x_or_o
    return board


def score_one_gamestate(board: np.array, x_or_o: str, available: list, ai_player_choice: str, score_dict=None,
                        weight=1) -> int:
    if score_dict is None:
        score_dict = {'wins': 0, 'losses': 0, 'draws': 0}
    is_finished = game_over(board)

    if is_finished == ai_player_choice:  # This might be wrong, we want ai_player_choice
        score_dict['wins'] += 1 / weight
        return score_dict
    elif is_finished == turn_flipper(ai_player_choice):
        score_dict['losses'] += 1 / weight
        return score_dict
    elif is_finished == 'draw':
        score_dict['draws'] += 1 / weight
        return score_dict
    else:
        weight *= len(available)
        for candidate_move in available:
            deeper = copy.deepcopy(board)
            deeper[candidate_move] = x_or_o
            available_moves = find_available_moves(deeper)
            score_dict = score_one_gamestate(deeper,
                                             turn_flipper(x_or_o),
                                             available_moves,
                                             ai_player_choice,
                                             score_dict,
                                             weight)
    return score_dict


def optimal_ai_move(board: np.array, x_or_o: str, available: list):
    """
    The heart of the robot brain.
    Given a board state, will return the optimal move.
    :param board: numpy array of the board.
    :param x_or_o: which side is the AI playing on? #This isn't exactly true in recursive calls.
    :param available: available[(row, col)] = True, if the space hasn't been taken yet.
    :return: best_move: (row, col). The move with the greatest number of simulated wins.
    """
    possibility_dict = {}
    for candidate_move in available:
        deeper = copy.deepcopy(board)
        deeper[candidate_move] = x_or_o
        available = find_available_moves(deeper)
        possibility_dict[candidate_move] = score_one_gamestate(deeper,
                                                               turn_flipper(x_or_o),
                                                               available,
                                                               x_or_o,
                                                               score_dict=None)

    metric_dict = {candidate_move: (score_dict['wins'] + score_dict['draws']) / sum(score_dict.values())
                   for candidate_move, score_dict in possibility_dict.items()}

    best_move = max(metric_dict, key=metric_dict.get)
    return best_move, possibility_dict


def find_available_moves(board: np.array) -> list:
    not_x_mask: np.array = board != 'x'
    not_o_mask: np.array = board != 'o'
    neither_mask: np.array = np.logical_and(not_x_mask, not_o_mask)
    available = [(i, j) for i in range(3) for j in range(3) if neither_mask[(i, j)]]
    return available


def ai_turn(board: np.array, x_or_o: str) -> np.array:
    # First policy is random policy, it randomly decides to pick from the available spaces.
    print("bleep bloop, now it is my turn")

    policy = 'optimal'
    available = find_available_moves(board)

    if policy == 'random':
        next_move = random.choice(available)

    if policy == 'optimal':
        if len(available) == 9:
            next_move = (1, 1)  # Really hacky memoisation, solving the first move takes 120 seconds otherwise.
        elif 6 < len(available) < 9:
            time.sleep(0.1)
            next_move = optimal_ai_move(board, x_or_o, available)[0]
        else:
            time.sleep(0.3)
            next_move = optimal_ai_move(board, x_or_o, available)[0]
    board[next_move] = x_or_o
    return board


def game_over(board: np.array) -> str:
    """
    Reads board to determine whether x, o, or a draw has occurred.
    :param board:
    :return: scenario "" = False, game not finished, 'x'=x_won, 'o'=o_won, 'draw'=draw
    """
    mask = {
        'x': board == 'x',  # Boolean mask of all the squares x resides in.
        'o': board == 'o'
    }

    for x_or_o, v in mask.items():
        has_winning_row = np.any(np.all(v, axis=1))
        has_winning_col = np.any(np.all(v, axis=0))
        has_winning_diagonal = np.all(v.diagonal())
        has_winning_off_diagonal = np.all(np.fliplr(v).diagonal())

        if has_winning_row or has_winning_col or has_winning_diagonal or has_winning_off_diagonal:
            return x_or_o

    if np.all(mask['x'] + mask['o']):  # all the squares are filled.
        return 'draw'

    else:
        return ""


def game_loop() -> None:
    """
    :return: None.
    """
    num_players = ''
    human_player_choice = ''

    while num_players not in ('0', '1', '2'):
        num_players = input("Number of players: ")
    board = np.array(
        [["e", "r", "t"], ["d", "f", "g"], ["c", "v", "b"]]
    )
    whose_turn = 'x'

    if num_players == '0':
        print("Ah, you would like to see robots compete for your entertainment. Sit back for two minutes and enjoy.")
        while not (game_over(board)):
            print(show_board(ai_turn(board, whose_turn)))
            whose_turn = turn_flipper(whose_turn)

    if num_players == '1':
        while human_player_choice not in ('x', 'o'):
            human_player_choice = input("Would you like to play as x or o: ")
        ai_player_choice = turn_flipper(human_player_choice)

        print("Welcome player " + human_player_choice)
        print(show_board(board))

        while not (game_over(board)):
            if whose_turn == human_player_choice:
                print(show_board(human_turn(board, human_player_choice)))
                whose_turn = turn_flipper(whose_turn)
            elif whose_turn != human_player_choice:
                print(show_board(ai_turn(board, ai_player_choice)))
                whose_turn = turn_flipper(whose_turn)

    if num_players == '2':
        print(show_board(board))
        while not (game_over(board)):
            print(show_board(human_turn(board, whose_turn)))
            whose_turn = turn_flipper(whose_turn)

    not_x_mask: np.array = board != 'x'
    not_o_mask: np.array = board != 'o'
    neither_mask: np.array = np.logical_and(not_x_mask, not_o_mask)
    print(show_board(np.where(neither_mask, ' ', board)))
    print(game_over(board))


if __name__ == "__main__":
    game_loop()
