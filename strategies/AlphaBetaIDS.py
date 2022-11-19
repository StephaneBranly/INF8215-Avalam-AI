import math
import time
from .AlphaBeta import AlphaBeta


class AlphaBetaIDS(AlphaBeta):

    def __init__(self):
        self.trimming_ratio = {6:{2:4.43,3:28.68},8:{2:3.62,3:32.08},10:{2:3.62,3:27.12},12:{2:4.33,3:26.17,4:4.32},13:{2:2.94},14:{2:3.77,3:22.14,4:3.82},15:{2:4.97},16:{2:4.0,3:18.92,4:2.62,5:9.13},17:{2:3.53},18:{2:3.48,3:17.09,4:3.9,5:6.9},19:{2:3.57},20:{2:3.65,3:16.19,4:3.36,5:6.65},21:{2:4.0,3:10.47},22:{2:3.24,3:11.12,4:2.92,5:5.91,6:2.84,7:3.76},23:{2:3.56,3:9.05,4:2.51},24:{2:3.27,3:9.0,4:2.32,5:5.2,6:2.36,7:2.4},25:{2:5.26,3:6.77,4:2.56},26:{2:3.14,3:6.09,4:2.41,5:3.47,6:1.63,7:1.87,8:0.43},27:{2:3.73,3:4.5,4:2.31,5:3.8,6:1.19,7:2.04},28:{2:2.84,3:4.02,4:1.87,5:2.02,6:1.16,7:0.75,8:0.85},29:{2:2.57,3:3.03,4:1.97,5:2.35,6:2.57,7:0.87,8:1.06},30:{2:2.35,3:2.18,4:1.23,5:0.89,6:0.95,7:0.99,8:1.0},31:{2:2.43,3:2.35,4:1.42,5:0.76,6:1.17,7:1.03,8:0.91},32:{2:1.39,3:0.84,4:0.93,5:0.97,6:1.0,7:0.88,8:0.68},33:{2:1.08,3:1.22,4:0.84,5:1.05,6:1.05,7:0.93,8:0.91},34:{2:0.87,3:0.72,4:0.98,5:0.6,6:0.5,7:0.88,8:1.37},36:{2:0.57,3:0.87,4:1.0,5:1.0}}
        super().__init__()

    def need_trimming(self,step,depth,start,time_to_play,last_time):
        time_remaining = time_to_play - (time.time() - start)
        if depth <= 1 or depth > 8:
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
        
        last_time = 0
        while(time.time()-start<time_to_play and max_depth<max_step and( player ==1 or not self.need_trimming(step,max_depth,start,time_to_play,last_time))):
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