from heuristic.Genetic1Action import Genetic1Action
from heuristic.observation_function import *

all_functions = [isolate_tower, ennemy_isolate_tower, mult_create_tower5,mult_create_tower4, mult_create_tower3, mult_create_tower2, enemy_mult_create_tower5, enemy_mult_create_tower4, enemy_mult_create_tower3, enemy_mult_create_tower2,score_after_action, remaining_actions]


class GeneticMultAction(Genetic1Action):
    def __init__(self, functions=None, parameters=None):
        super().__init__(functions, parameters, all_functions=all_functions)
        
    def evaluate(self,init_board,current_board,player,action):
        score = 0

        for i in range(len(self._functions)):
            score += self._parameters[i]*self._functions[i]([init_board,current_board],player,action)
        return score

    def clone(self):
        return GeneticMultAction(self._functions,self._parameters)