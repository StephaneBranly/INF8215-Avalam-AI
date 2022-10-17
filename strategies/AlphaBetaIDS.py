import math
import time
from .AlphaBeta import AlphaBeta


class AlphaBetaIDS(AlphaBeta):

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):

        start = time.time()

        hashMaps = []
        for i in range(0, 40):
            hashMaps.append({})


        init_board = board.clone()


        heuristic = other_params['heuristic']
        max_depth = 0
        while time.time()-start < time_to_play:
            max_depth += 1
            _, m, explored, hash_reduced, transposition = self.max_value(board, init_board, heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play, 0, 0, 0)
        if stats:
            print(f"AlphaBeta hash_reduced {hash_reduced} | transposition {transposition} | explored {explored} | depth {max_depth} | time {time.time()-start}")
        return m