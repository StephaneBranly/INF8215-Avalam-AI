from heuristic.GeneticHeuristic import GeneticHeuristic
from heuristic.observation_function import *

all_single_loop_functions = [single_loop_isolated_tower, enemy_single_loop_isolated_tower, single_loop_tower5, single_loop_tower4, single_loop_tower3, single_loop_tower2, enemy_single_loop_tower5, enemy_single_loop_tower4, enemy_single_loop_tower3, enemy_single_loop_tower2]

"""
    This genetic Agent use a single loop to evaluate the board.
"""

class GeneticSingleLoop(GeneticHeuristic):
    def __init__(self, functions=None, parameters=None):
        """
            If functions and parameters are None, the agent will be initialized with random parameters and a sample of functions from all available functions.
            arguments:
                functions -- list of functions to use
                parameters -- list of parameters to use
        """
        super().__init__(functions, parameters, all_functions=all_single_loop_functions)

    def evaluate(self,board,player,action):
        """
            Evaluate the board for the player in a single loop
        """
        score = 0
        for i in range(9):
            for j in range(9):
                for k in range(len(self._functions)):
                    score += self._parameters[k]*self._functions[k](board,player,i,j)
        return score

    def clone(self):
        return GeneticSingleLoop(self._functions,self._parameters)