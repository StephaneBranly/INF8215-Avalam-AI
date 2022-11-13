import math
import time

from avalam import EvolvedAgent
from .AlphaBeta import AlphaBeta


class AlphaBetaIDS(AlphaBeta):

    def nextStepPossible(self,max_depth, time_to_play,last_time,start):
        if max_depth == 2 and time_to_play - (time.time()-start) < last_time * 3.5:
            return False
        if max_depth == 3 and time_to_play - (time.time()-start) < last_time * 10:
            return False
        return True

    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):

        start = time.time()
        
        heuristic = other_params['heuristic']
        max_step = other_params['max_step']
        max_depth = 0
        last_time = 0
        print("-------------Step", step, "-------------")
        while(time.time()-start<time_to_play and max_depth<max_step):
            new_start = time.time()
            max_depth+=1
            hashMaps = []
            for i in range(0, 40):
                hashMaps.append({})

            _, m, explored, hash_reduced, transposition = self.max_value(board.clone(), heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play)
            
            last_time = time.time()-new_start

            print("Depth: ", max_depth, "Time: ", time.time()-new_start,"action", m,"explored", explored,"hashReduced",hash_reduced,"transposition",transposition)
            
            if(time.time()-start<time_to_play):
                action = m
                # open csv file and write step, depth and time
                """if step > 16 and max_depth > 1:
                    with open('stats/time.csv', 'a') as f:
                            f.write(str(step)+','+str(max_depth)+','+str(time.time()-new_start)+'\n')"""
            
            

        return action