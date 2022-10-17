from heuristic.GeneticHeuristic import GeneticHeuristic
from heuristic.observation_function import *

all_functions = [finish_tower, isolate_tower, ennemy_isolate_tower, use_token, cover_token, create_tower4, create_tower3, create_tower2, score_after_action, remaining_actions]

class Genetic1Action(GeneticHeuristic):
    def __init__(self, functions=None, parameters=None):
        super().__init__(functions, parameters, all_functions=all_functions)

    def evaluate(self,board,player,action):
        score = 0
        next_board = board.clone()
        next_board.play_action(action)
        for i in range(len(self._functions)):
            score += self._parameters[i]*self._functions[i]([board, next_board],player,action)
        return score
    
    def clone(self):
        return Genetic1Action(self._functions,self._parameters)

    
