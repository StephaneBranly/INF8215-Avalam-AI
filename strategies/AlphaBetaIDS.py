import math
import time
from .AlphaBeta import AlphaBeta


class AlphaBetaIDS(AlphaBeta):

    def __init__(self):
        self.trimming_ratio = {14:{2:3.77,3:22.14,4:3.29},16:{2:4.0,3:20.01,4:2.54},18:{2:3.48,3:18.58,4:3.18},20:{2:3.66,3:16.56,4:3.36},22:{2:3.27,3:11.34,4:2.74,5:5.91,6:2.78,7:3.76},24:{2:3.33,3:9.06,4:2.31,5:5.43,6:2.36,7:2.4},26:{2:3.14,3:6.27,4:2.37,5:3.68,6:1.62,7:1.55},28:{2:2.82,3:4.19,4:1.88,5:1.95,6:1.16,7:0.7},30:{2:2.35,3:2.05,4:1.23,5:0.88,6:0.96,7:0.99},32:{2:1.39,3:0.81,4:0.93,5:0.97,6:1.0,7:0.88},34:{2:0.87,3:0.54,4:0.98,5:0.51,6:0.5,7:1.0},36:{2:0.57,3:0.87,4:1.0,5:1.0}}
        super().__init__()

    def need_trimming(self,step,depth,start,time_to_play,last_time):
        return False
        time_remaining = time_to_play - (time.time() - start)
        if step <= 10 or depth <= 1 or depth > 7:
            return False
        for i in range(step,37):
            if(i in self.trimming_ratio and depth in self.trimming_ratio[i]):
                return self.trimming_ratio[i][depth] * last_time > time_remaining
        return False


    def use_strategy(self, board, player, step, time_to_play, stats=False, other_params=None):

        start = time.time()
        print("step", step, "time", time_to_play)
        heuristic = other_params['heuristic']
        max_step = other_params['max_step']
        max_depth = 0
        if  step <= 5:
            max_step = 1
        elif step <= 10:
            max_step = 4
        elif step <= 15:
            max_step = 5
        elif step <= 20:
            max_step = 6
        elif step <= 25:
            max_step = 7
        last_time = 0
        while(time.time()-start<time_to_play and max_depth<max_step):
            new_start = time.time()
            max_depth+=1
            hashMaps = []
            for i in range(0, 40):
                hashMaps.append({})

            _, m, explored, hash_reduced, transposition = self.max_value(board.clone(), heuristic, player, -math.inf, math.inf, 0, max_depth, hashMaps, start, step, time_to_play)
            print("Depth: ", max_depth, "Time: ", time.time()-new_start,"action", m,"explored", explored,"hashReduced",hash_reduced,"transposition",transposition)
            last_time = time.time()-new_start
            if(time.time()-start<time_to_play):
                action = m
                if step > 5 and max_depth >1:
                    with open('stats/time.csv', 'a') as f:
                        f.write(str(step)+","+str(max_depth)+","+str(time.time()-new_start)+"\n")


        return action