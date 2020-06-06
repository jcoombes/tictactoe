import tictactoe as ttt
import numpy as np

board = np.array([
    ['o', 'x', 't'],
    ['d', 'x', 'g'],
    ['o', 'v', 'b']
])

available = ttt.find_available_moves(board)

best_move, metric_dict = ttt.optimal_ai_move(board=board, x_or_o='x', available=available)
print(best_move, metric_dict)

"""
The AI chooses bottom left - (0, 2) here. This means the human can choose bottom middle - (1,2) and win.

So what's going on here?
The AI is not making any assumptions about what kind of player it is against,
and just counts the number of wins and losses, without prioritising some moves as more likely  than others.
 
 So policy='optimal' is actually optimal against a random player. 
 
 I can fix this by adding a 'weight' term, to value wins, losses, draws now
  more highly than wins, losses draws later.
"""