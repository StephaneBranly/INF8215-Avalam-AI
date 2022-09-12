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
import json

from heuristic.heuristic import Genetic_1_action_heuristique


class MyAgent(Agent):
    def initialize(self, percepts, players, time_left):
        return super().initialize(percepts, players, time_left)

    def __init__(self):
        pass

    def setup(self, agent, parser, args):
        self.current_individu = None
        self.current_gen = 0
        self.heuristic = Genetic_1_action_heuristique()
        self.load_best_individu()

    def load_best_individu(self):
        try:
            with open(f"NN_heuristic/gen{self.current_gen}.json") as fp:
                listObj = json.load(fp)
            scores = [cell['score'] for cell in listObj['gen']]
            self.current_individu = np.argmax(scores)
            self.heuristic.load_from_json(f"NN_heuristic/gen{self.current_gen}.json", self.current_individu)
        except:
            print('No more generation')

        
    def play(self, percepts, player, step, time_left):

        board = dict_to_board(percepts)
        best_action = ()
        best_score = -99999999
        
        for action in board.get_actions():
            if self.heuristic.evaluate(board, player, action) > best_score:

                best_score = self.heuristic.evaluate(board, player, action)
                best_action = action

        return best_action

      


  
    def get_agent_id(self):
        """Return an identifier for this agent."""
        return f"tiktok #{self.current_individu} G{self.current_gen}"

    def pool_ended(self, pool, player):
        self.current_gen += 1
        self.load_best_individu()
        return super().pool_ended(pool, player)

if __name__ == "__main__":
    def argument_parser(agent, parser):
        parser.add_argument("-I", "--individu", default=0, help="index of the individu to take", type=int)
        parser.add_argument("-G", "--generation", default=0, help="generation to take", type=int)
    agent = MyAgent()
    agent_main(agent, argument_parser, agent.setup)



