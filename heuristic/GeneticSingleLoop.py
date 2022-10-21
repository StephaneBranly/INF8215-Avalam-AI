from heuristic.GeneticHeuristic import GeneticHeuristic
from heuristic.observation_function import *

all_single_loop_functions = [single_loop_isolated_tower,enemy_single_loop_isolated_tower,single_loop_tower5,single_loop_tower4,single_loop_tower3,single_loop_tower2,enemy_single_loop_tower5,enemy_single_loop_tower4,enemy_single_loop_tower3,enemy_single_loop_tower2,single_loop_isolated_tower5,single_loop_isolated_tower4,single_loop_isolated_tower3,single_loop_isolated_tower2,enemy_single_loop_isolated_tower5,enemy_single_loop_isolated_tower4,enemy_single_loop_isolated_tower3,enemy_single_loop_isolated_tower2,wineable_tower,enemy_wineable_tower,score,remaining_actions]
all_whole_board_functions = [score, remaining_actions]
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
            We consider that the first functions are single loop and the lasts are whole board
        """
        score = 0
        start_index_whole_board = len(self._functions)
        for (i,j) in board.get_real_board():
                isolated = not board.is_tower_movable(i,j)
                for k in range(len(self._functions)):

                    if self._functions[k] in all_whole_board_functions:
                        start_index_whole_board = k
                        break

                    score += self._parameters[k]*self._functions[k](board,player,i,j,isolated)
        #print(start_index_whole_board,len(self._functions),len(self._parameters))
        for k in range(start_index_whole_board,len(self._functions)):
            score += self._parameters[k]*self._functions[k](board,player)
        return score

    def clone(self):
        return GeneticSingleLoop(self._functions,self._parameters)