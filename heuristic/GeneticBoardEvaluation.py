from heuristic.GeneticHeuristic import GeneticHeuristic
from heuristic.observation_function import *

all_board_evaluation_functions = [
    board_score,
    board_tower5,
    board_tower4,
    board_tower3,
    board_tower2,
    board_tower1,
    board_tower5_negative,
    board_tower4_negative,
    board_tower3_negative,
    board_tower2_negative,
    board_tower1_negative,
    board_isolated_tower5,
    board_isolated_tower4,
    board_isolated_tower3,
    board_isolated_tower2,
    board_isolated_tower1,
    board_isolated_tower5_negative,
    board_isolated_tower4_negative,
    board_isolated_tower3_negative,
    board_isolated_tower2_negative,
    board_isolated_tower1_negative,
    board_towers_links_1_1,
    board_towers_links_1_2,
    board_towers_links_1_3,
    board_towers_links_1_4,
    board_towers_links_2_2,
    board_towers_links_2_3,
    board_towers_links_1_1_negative,
    board_towers_links_1_2_negative,
    board_towers_links_1_3_negative,
    board_towers_links_1_4_negative,
    board_towers_links_2_2_negative,
    board_towers_links_2_3_negative,
    board_towers_links_1_1_different,
    board_towers_links_1_2_different,
    board_towers_links_1_3_different,
    board_towers_links_1_4_different,
    board_towers_links_2_2_different,
    board_towers_links_2_3_different,
    ]
"""
    This genetic Agent use board functions.
"""

class GeneticBoardEvaluation(GeneticHeuristic):
    def __init__(self, functions=None, parameters=None):
        """
            If functions and parameters are None, the agent will be initialized with random parameters and a sample of functions from all available functions.
            arguments:
                functions -- list of functions to use
                parameters -- list of parameters to use
        """
        super().__init__(functions, parameters, all_functions=all_board_evaluation_functions)

    def evaluate(self,board,player,action):
        """
            Evaluate the board for the player in a single loop
            We consider that the first functions are single loop and the lasts are whole board
        """
        score = 0
        for k in range(len(self._functions)):
            score += self._parameters[k]*self._functions[k](board) * player
        return score

    def clone(self):
        return GeneticBoardEvaluation(self._functions,self._parameters)