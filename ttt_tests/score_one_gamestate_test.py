import tictactoe as ttt
import numpy as np

board = np.array([
    ['o', 'x', 't'],
    ['d', 'x', 'g'],
    ['c', 'v', 'b']
])

available = ttt.find_available_moves(board)

score_dict = ttt.score_one_gamestate(board=board, x_or_o='o', available=available, ai_player_choice='x')
print(score_dict)
# google says 25168 possible boards, 131184 are wins, 77904 are losses and 46080 are draws.
