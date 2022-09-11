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
import numpy as np
import random
import json
import itertools
from heuristic.heuristic import Genetic_1_action_heuristique

class MyAgent(Agent):
    def initialize(self, percepts, players, time_left):
        return super().initialize(percepts, players, time_left)

    def __init__(self):
        pass

    def setup(self, agent, parser, args):
        self.nb_individu = args.individu
        self.gen = args.generation
        self.current_individu = None
        self.current_gen = 0
        self.heuristic_p1 = Genetic_1_action_heuristique()
        self.heuristic_m1 = Genetic_1_action_heuristique()
        self.added_players = []

        self.matchs = [m for m in itertools.combinations(range(self.nb_individu), 2)]

        self.current_match = None
        self.scores = dict()
        for a in range(self.nb_individu):
            self.scores[a] = 0
        self.load_match()




        
    def play(self, percepts, player, step, time_left):

        board = dict_to_board(percepts)
        best_action = ()
        best_score = -99999999
        heuristic = None
        if player == 1:
            heuristic = self.heuristic_p1
        else:
            heuristic = self.heuristic_m1

        for action in board.get_actions():
            if heuristic.evaluate(board, player, action) > best_score:

                best_score = heuristic.evaluate(board, player, action)
                best_action = action

        return best_action



    

    


    def get_agent_id(self):
        """Return an identifier for this agent."""
        return f"Best genetic player (#{self.current_individu}) of generation {self.current_gen}"

    def finished(self, steps, winner, reason="", player=None):
        player_winner = 0 if winner < 0 else 1 if winner > 0 else None
        if player == 1:
            if winner != 0:
                self.scores[self.current_match[player_winner]] += abs(winner)
                self.scores[self.current_match[1-player_winner]] -= abs(winner)
            if len(self.matchs):
                self.load_match()

    def load_match(self):
        self.current_match = self.matchs.pop(0)
        if self.gen == 0: # case of the first generation, we create random NN
            if len(self.added_players) == 0: # first individu added, we generate a new file
                f = open(f"NN_heuristic/gen{self.gen}.json", "w")
                f.write('{ \"gen\": []}')
                f.close()
            if self.current_match[0] not in self.added_players: # we add player -1 if not already added
                self.heuristic_m1 = Genetic_1_action_heuristique()
                self.heuristic_m1.save_as_json(f"NN_heuristic/gen{self.gen}.json", self.current_match[0])
                self.added_players.append(self.current_match[0])
            if self.current_match[1] not in self.added_players: # we add player 1 if not already added
                self.heuristic_p1 = Genetic_1_action_heuristique()
                self.heuristic_p1.save_as_json(f"NN_heuristic/gen{self.gen}.json", self.current_match[1])
                self.added_players.append(self.current_match[1])
        else: # case of the next generations, we load the NN of the previous generation
            self.heuristic_m1.load_from_json(f"NN_heuristic/gen{self.gen}.json", self.current_match[0])
            self.heuristic_p1.load_from_json(f"NN_heuristic/gen{self.gen}.json", self.current_match[1])

    def save_stats(self):
        with open(f"NN_heuristic/gen{self.gen}.json") as f:
            listObj = json.load(f)
            for i in range(self.nb_individu):
                listObj["gen"][i]["score"] = self.scores[i]
        with open(f"NN_heuristic/gen{self.gen}.json", 'w') as outfile:
            json.dump(listObj, outfile)

    def pool_ended(self, pool, player):
        if player == 1:
            print(self.scores)
            self.save_stats()
            results = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
            f = open(f"NN_heuristic/gen{self.gen+1}.json", "w")
            f.write('{ \"gen\": []}')
            f.close()
            for l in range(self.nb_individu):
                father = Genetic_1_action_heuristique()
                father.load_from_json(f"NN_heuristic/gen{self.gen}.json", results[random.randint(0, self.nb_individu//10)][0])
                mother = Genetic_1_action_heuristique()
                mother.load_from_json(f"NN_heuristic/gen{self.gen}.json", results[random.randint(0, self.nb_individu//10)][0])
                child = father.crossover(mother)
                child.mutate(0.1)
                
                child.save_as_json(f"NN_heuristic/gen{self.gen+1}.json", l)
            self.gen += 1

            self.matchs = [m for m in itertools.combinations(range(self.nb_individu), 2)]

            self.current_match = None
            self.scores = dict()
            for a in range(self.nb_individu):
                self.scores[a] = 0
            self.load_match()
        return super().pool_ended(pool, player)

if __name__ == "__main__":
    def argument_parser(agent, parser):
        parser.add_argument("-I", "--individu", default=10, help="number of individu in the pool", type=int)
        parser.add_argument("-G", "--generation", default=0, help="initial generation", type=int)
    agent = MyAgent()
    agent_main(agent, argument_parser, agent.setup)
