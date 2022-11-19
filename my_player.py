#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import time
from avalam import *
from heuristic import *
from ImprovedBoard import *
import math




class MyAgent(Agent):

    def __init__(self):
        self.trimming_ratios = {6:{2:4.43,3:28.68},8:{2:3.62,3:32.08},10:{2:3.62,3:27.12},12:{2:4.33,3:26.17,4:4.32},13:{2:2.94},14:{2:3.77,3:22.14,4:3.82},15:{2:4.97},16:{2:4.0,3:18.92,4:2.62,5:9.13},17:{2:3.53},18:{2:3.48,3:17.09,4:3.9,5:6.9},19:{2:3.57},20:{2:3.65,3:16.19,4:3.36,5:6.65},21:{2:4.0,3:10.47},22:{2:3.24,3:11.12,4:2.92,5:5.91,6:2.84,7:3.76},23:{2:3.56,3:9.05,4:2.51},24:{2:3.27,3:9.0,4:2.32,5:5.2,6:2.36,7:2.4},25:{2:5.26,3:6.77,4:2.56},26:{2:3.14,3:6.09,4:2.41,5:3.47,6:1.63,7:1.87,8:0.43},27:{2:3.73,3:4.5,4:2.31,5:3.8,6:1.19,7:2.04},28:{2:2.84,3:4.02,4:1.87,5:2.02,6:1.16,7:0.75,8:0.85},29:{2:2.57,3:3.03,4:1.97,5:2.35,6:2.57,7:0.87,8:1.06},30:{2:2.35,3:2.18,4:1.23,5:0.89,6:0.95,7:0.99,8:1.0},31:{2:2.43,3:2.35,4:1.42,5:0.76,6:1.17,7:1.03,8:0.91},32:{2:1.39,3:0.84,4:0.93,5:0.97,6:1.0,7:0.88,8:0.68},33:{2:1.08,3:1.22,4:0.84,5:1.05,6:1.05,7:0.93,8:0.91},34:{2:0.87,3:0.72,4:0.98,5:0.6,6:0.5,7:0.88,8:1.37},36:{2:0.57,3:0.87,4:1.0,5:1.0}}

        self.heuristic_core = heuristic()
        super().__init__()

    def need_trimming(self,step,depth,start,time_to_play,last_time):
        time_remaining = time_to_play - (time.time() - start)
        if depth > 1 and depth <= 8:
            for i in range(step,37):
                if(i in self.trimming_ratios and depth in self.trimming_ratios[i]):
                    return self.trimming_ratios[i][depth] * last_time > time_remaining
        return False

    def play(self, percepts, player, step, time_left):

        start = time.time()
        time_to_play = time_left/((34-step)/2) if step < 34 else time_left/2
        board = dict_to_improved_board(percepts,True)



        if step <= 5:
            max_depth = 1
        else:
            max_depth = 15
        
        depth = 0
        last_time = 0

        while time.time()-start<time_to_play and depth<max_depth and not self.need_trimming(step,depth,start,time_to_play,last_time):

            new_start = time.time()
            depth += 1
            hashMaps = []
            for i in range(0, 40):
                hashMaps.append({})
            v, m = self.max(board, player, -math.inf, math.inf, 0, depth, hashMaps, start, time_to_play)
            last_time = time.time()-new_start
            if(time.time()-start<time_to_play or depth==1):
                action = m


        return action

    def min(self, board, player, alpha, beta, depth, max_depth, hash_maps, start, time_to_play):
        
        v,m = self.trivial_case(board, player, depth, max_depth, hash_maps, start, time_to_play)
        if v is not None:
            return (v,m)

        v,m = (math.inf,None)

        actions = [a for a in board.get_actions()]
        actions.sort(key=lambda a: self.sort_evaluate(board, a, player), reverse=False)

        for a in actions:
            board.play_action(a)
            nV, _ = self.max(board, player, alpha, beta, depth+1, max_depth, hash_maps, start, time_to_play)
            board.undo_action()
            if nV < v:
                v = nV
                m = a
                beta = min(beta, v)
            if v <= alpha:
                self.save_hash(board, depth, hash_maps, v, m)
                return (v,m)

        self.save_hash(board, depth, hash_maps, v, m)

        return (v,m)

    def max(self, board, player, alpha, beta, depth, max_depth, hash_maps, start, time_to_play):
        v,m = self.trivial_case(board, player, depth, max_depth, hash_maps, start, time_to_play)
        if v is not None:
            return (v,m)
        
        v,m = (-math.inf,None)

        actions = [a for a in board.get_actions()]
        actions.sort(key=lambda a: self.sort_evaluate(board, a, player), reverse=True)

        for a in actions:
            board.play_action(a)
            nV, _ = self.min(board, player, alpha, beta, depth+1, max_depth, hash_maps, start, time_to_play)
            board.undo_action()
            if nV > v:
                v = nV
                m = a
                alpha = max(alpha, v)
            if v >= beta:
                self.save_hash(board, depth, hash_maps, v, m)
                return (v,m)

        self.save_hash(board, depth, hash_maps, v, m)

        return (v,m)


    def save_hash(self, board, depth, hash_maps, v, m):
        if depth > 1:
            hash = board.get_hash()
            hash_maps[depth][hash] = (v,m)
        

    def sort_evaluate(self,board,action,player):
        board.play_action(action)
        v = self.heuristic(board,player)
        board.undo_action()
        return v

    def trivial_case(self, board, player, depth, max_depth, hash_maps, start, time_to_play):

        # partie terminée 
        if board.is_finished():
            return (math.inf*player*board.get_score(),None)
        
        # fin exploration
        if depth >= max_depth or time.time()-start > time_to_play:
            return (self.heuristic(board,player),None)
        
        # etat deja visité 
        if depth >= 1:
            h = board.get_hash()
            if h in hash_maps[depth]:
                return (hash_maps[depth][h][0],hash_maps[depth][h][1])

        return (None,None)

    def heuristic(self, board, player) -> float:
        return self.heuristic_core(board,player)





if __name__ == "__main__":
    agent_main(MyAgent())

