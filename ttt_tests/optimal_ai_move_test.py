import tictactoe as ttt
import numpy as np

board = np.array([
    ['e', 'r', 't'],
    ['d', 'f', 'g'],
    ['c', 'v', 'b']
])

available = ttt.find_available_moves(board)

metric_dict = ttt.optimal_ai_move(board=board, x_or_o='x', available=available)
print(metric_dict)
# Finally, a clear demonstration that going in the middle wins more often than other locations.
