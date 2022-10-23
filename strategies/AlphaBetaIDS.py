import math
import time
from .AlphaBeta import AlphaBeta


class AlphaBetaIDS(AlphaBeta):

    def loopingIDS(self,board,heuristic, player,max_depth, hashMaps, start, step, time_to_play,last = None):
        new_start = time.time()
        hashMaps = []
        for i in range(0, 40):
            hashMaps.append({})
        _, m, explored, hash_reduced, transposition = self.max_value(board.clone(), heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play)
        print("Max Step",step+max_depth,"Depth: ", max_depth, "Time: ", time.time()-new_start,"action", m)
        if(time.time()-start>time_to_play or max_depth>20):
            return last,max_depth
        else:
            return self.loopingIDS(board,heuristic, player,max_depth+1, hashMaps, start, step, time_to_play,m)

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):

        start = time.time()
        
        heuristic = other_params['heuristic']
        max_step = other_params['max_step']
        max_depth = 0
        while(time.time()-start<time_to_play and max_depth<max_step):
            new_start = time.time()
            max_depth+=1
            hashMaps = []
            for i in range(0, 40):
                hashMaps.append({})

            _, m, explored, hash_reduced, transposition = self.max_value(board.clone(), heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play)
            print("Depth: ", max_depth, "Time: ", time.time()-new_start,"action", m,"explored", explored,"hashReduced",hash_reduced,"transposition",transposition)
            
            if(time.time()-start<time_to_play):
                action = m

        """hashMaps = []
        for i in range(0, 40):
            hashMaps.append({})
        print("Final step: ", step+max_depth-1)
        new_start = time.time()
        _, m, _, _,_ = self.max_value(board, heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, 100000000)
        print("Time for next depth: ", time.time()-new_start, "action", m)"""
        """if stats:
            print(f"AlphaBeta hash_reduced {hash_reduced} | transposition {transposition} | explored {explored} | depth {max_depth} | time {time.time()-start}")"""
        return action