import math
import Strategy

class BestMove(Strategy):
    def __init__(self):
        super().__init__()

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):
        best_action = ()
        best_score = -math.inf
        
        for action in board.get_actions():
            current_score = self.evaluate(board, player, action)
            if current_score > best_score:
                best_score = current_score
                best_action = action

        return best_action