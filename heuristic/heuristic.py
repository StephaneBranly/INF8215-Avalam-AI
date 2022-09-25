from .observation_function import *
import random
import json

class Heuristic:
    def __init__(self):
        pass

    def evaluate(self,board,player,action):
        raise NotImplementedError

    def interprete_params(self):
        return None

    def __call__(self,board,player,action):
        return self.evaluate(board,player,action)

default_functions = [finish_tower, isolate_tower, ennemy_isolate_tower, use_token, cover_token, create_tower4, create_tower3, create_tower2, score_after_action, remaining_actions]

class Genetic_1_action_heuristique(Heuristic):
    def __init__(self, functions=default_functions, parameters=None):
        self._parameters = [random.uniform(-1,1) for parameters in range(len(functions))]
        if parameters is not None:
            self._parameters = parameters
        self._functions = functions

    def evaluate(self,board,player,action):
        score = 0
        next_board = board.clone()
        next_board.play_action(action)
        for i in range(len(self._functions)):
            score += self._parameters[i]*self._functions[i]([board, next_board],player,action)
        return score

    def interprete_params(self):
        return [f.__name__ for f in self._functions]
    
    def set_parameters(self,parameters):
        self._parameters = parameters
    
    def get_parameters(self):
        return self._parameters

    def mutate(self,mutation_rate):
        for i in range(len(self._parameters)):
            if random.random() < mutation_rate:
                self._parameters[i] += random.uniform(-1,1)
                if self._parameters[i] > 1:
                    self._parameters[i] = 1
                elif self._parameters[i] < -1:
                    self._parameters[i] = -1

    def crossover(self,other):
        new_parameters = []
        for i in range(len(self._parameters)):
            if random.random() < 0.5:
                new_parameters.append(self._parameters[i])
            else:
                new_parameters.append(other.get_parameters()[i])
        return Genetic_1_action_heuristique(parameters=new_parameters)

    def save_as_json(self, filename, score):
        """Warning: no empty file : it needs to have a array called "gen" """
        with open(filename) as fp:
            listObj = json.load(fp)
        data = {}
        data['score'] = score
        data['parameters'] = self._parameters
        data['functions'] = [f.__name__ for f in default_functions if f in self._functions] # non optimal but safe way to save order functions and keep the same order when loading
        listObj["gen"].append(data)
        with open(filename, 'w') as outfile:
            json.dump(listObj, outfile)

    def load_from_json(self, filename, index):
        with open(filename) as fp:
            listObj = json.load(fp)
        self._parameters = listObj["gen"][index]["parameters"]
        self._functions = [f for f in default_functions if f.__name__ in listObj["gen"][index]["functions"]]
