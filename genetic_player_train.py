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
from avalam import *
from NN.neural_network import NN
import numpy as np
import random
import timeit
import itertools


class MyAgent(Agent):
    def initialize(self, percepts, players, time_left):
        return super().initialize(percepts, players, time_left)

    def __init__(self):
        self.nb_individu = 5
        self.gen = 0
        self.NN_p1 = NN([9,10,8])
        self.NN_m1 = NN([9,10,8])

        self.matchs = [m for m in itertools.combinations(range(self.nb_individu), 2)]

        self.current_match = None
        self.scores = dict()
        for a in range(self.nb_individu):
            self.scores[a] = 0
        self.load_match()
        
    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in avalam.py.
        :param player: the player to control in this step (-1 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
            eg; (1, 4, 1 , 3) to move tower on cell (1,4) to cell (1,3)
        """

        start = timeit.default_timer()

        # todo: iterating over all possible moves and choosing the best one (not only center of the board)
        m = percepts['m']
        actions = []

        for i in range(1,8):
            for j in range(1,8):
                """
                decision :
                0 1 2
                3   4
                5 6 7
                """

                NN = self.NN_p1 if player == 1 else self.NN_m1
                predict = NN.predict(np.array([m[i-1][j-1], m[i-1][j], m[i-1][j+1], m[i][j-1], m[i][j], m[i][j+1], m[i+1][j-1], m[i+1][j], m[i+1][j+1]]))

                for k in range(len(predict)):
                    if dict_to_board(percepts).is_action_valid(self.get_action(i,j,k)):
                        actions.append([predict[k],self.get_action(i,j,k)])
        if(len(actions) == 0):
            board = dict_to_board(percepts)
            return random.choice(list(board.get_actions()))

        action = self.get_best_action(actions,percepts)
        # print("action:", action)
        stop = timeit.default_timer()

        # print('Time: ', stop - start) 
        return action
    
    def get_action(self,i,j,decision):
        """
                decision :
                0 1 2
                3   4
                5 6 7
        """
        if decision == 0:
            return (i,j,i-1,j-1)
        elif decision == 1:
            return (i,j,i-1,j)
        elif decision == 2:
            return (i,j,i-1,j+1)
        elif decision == 3:
            return (i,j,i,j-1)
        elif decision == 4:
            return (i,j,i,j+1)
        elif decision == 5:
            return (i,j,i+1,j-1)
        elif decision == 6:
            return (i,j,i+1,j)
        elif decision == 7:
            return (i,j,i+1,j+1)
    
    def get_best_action(self,actions,percepts):
        best = actions[0]
        for action in actions:
            if action[0] > best[0]:
                best = action
        return best[1]
        
    def finished(self, steps, winner, reason="", player=None):
        player_winner = 0 if winner < 0 else 1 if winner > 0 else None
        print(winner)
        print(player)
        if player == 1:
            if winner != 0:
                self.scores[self.current_match[player_winner]] += abs(winner)
                self.scores[self.current_match[1-player_winner]] -= abs(winner)
            if len(self.matchs):
                self.load_match()
        # print(self.scores)

    def load_match(self):
        self.current_match = self.matchs.pop(0)
        self.NN_m1.load_from_json(f"NN/gen{self.gen}.json", self.current_match[0])
        self.NN_p1.load_from_json(f"NN/gen{self.gen}.json", self.current_match[1])

    def pool_ended(self, pool, player):
        if player == 1:
            print(self.scores)
            results = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
            f = open(f"NN/gen{self.gen+1}.json", "w")
            f.write('{ \"gen\": []}')
            f.close()
            for l in range(self.nb_individu):
                father = NN([9,10,8])
                father.load_from_json(f"NN/gen{self.gen}.json", results[0][0])
                mother = NN([9,10,8])
                mother.load_from_json(f"NN/gen{self.gen}.json", results[1][0])
                child = father.crossover(mother)
                child.mutate()
                
                child.save_as_json(f"NN/gen{self.gen+1}.json", l)
            self.gen += 1

            self.matchs = [m for m in itertools.combinations(range(self.nb_individu), 2)]

            self.current_match = None
            self.scores = dict()
            for a in range(self.nb_individu):
                self.scores[a] = 0
            self.load_match()
        return super().pool_ended(pool, player)

if __name__ == "__main__":
    agent_main(MyAgent())



