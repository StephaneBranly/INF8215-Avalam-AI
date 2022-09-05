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


class MyAgent(Agent):

    def __init__(self):

        self.NN = NN([9,10,8])

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
        print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

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

                predict = self.NN.predict(np.array([m[i-1][j-1], m[i-1][j], m[i-1][j+1], m[i][j-1], m[i][j], m[i][j+1], m[i+1][j-1], m[i+1][j], m[i+1][j+1]]))
                if dict_to_board(percepts).is_action_valid(self.get_action(i,j,predict[0])):
                    actions.append([predict[1],self.get_action(i,j,predict[0])])

        action = self.get_best_action(actions,percepts)
        print("action:", action)
        return action
    
    def get_action(self,i,j,decision):
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
        


if __name__ == "__main__":
    agent_main(MyAgent())



