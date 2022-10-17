from .observation_function import *
import random
import json

default_functions = [finish_tower, isolate_tower, ennemy_isolate_tower, use_token, cover_token, create_tower4, create_tower3, create_tower2, score_after_action, remaining_actions]
default_mult_functions = [isolate_tower, ennemy_isolate_tower, mult_create_tower5,mult_create_tower4, mult_create_tower3, mult_create_tower2, enemy_mult_create_tower5, enemy_mult_create_tower4, enemy_mult_create_tower3, enemy_mult_create_tower2,score_after_action, remaining_actions]
default_single_loop_functions = [single_loop_isolated_tower, enemy_single_loop_isolated_tower, single_loop_tower5, single_loop_tower4, single_loop_tower3, single_loop_tower2, enemy_single_loop_tower5, enemy_single_loop_tower4, enemy_single_loop_tower3, enemy_single_loop_tower2]
default_board_functions = [score_after_action, remaining_actions]

class Heuristic:
    def __init__(self):
        pass

    def evaluate(self,board,player,action):
        raise NotImplementedError

    def interprete_params(self):
        return None

    def __call__(self,board,player,action):
        return self.evaluate(board,player,action)

class Genetic_heuristic(Heuristic):
    def __init__(self, functions=None, parameters=None):
        self._parameters = [random.uniform(-1,1) for parameters in range(len(functions))]
        if parameters is not None:
            self._parameters = parameters
        self._functions = functions

    def evaluate(self):
        pass

    def interprete_params(self):
        return [f.__name__ for f in self._functions]

    def get_default_agent(self):
        return Genetic_heuristic(self._functions)
    
    def set_parameters(self,parameters):
        self._parameters = parameters
        return self
    
    def get_parameters(self):
        return self._parameters
    
    def mutate(self,mutation_rate):
        for i in range(len(self._parameters)):
            if random.random() < mutation_rate:
                self._parameters[i] *= random.uniform(-1,1)


    def crossover(self,other):
        new_parameters = []
        for i in range(len(self._parameters)):
            if random.random() < 0.5:
                new_parameters.append(self._parameters[i])
            else:
                new_parameters.append(other.get_parameters()[i])

        return self.get_default_agent().set_parameters(new_parameters)

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
        if "functions" in listObj["gen"][index]:
            self._functions = [f for f in default_functions if f.__name__ in listObj["gen"][index]["functions"]]


class Genetic_1_action_heuristic(Genetic_heuristic):
    def __init__(self, functions=default_functions, parameters=None):
        super().__init__(functions, parameters)

    def evaluate(self,board,player,action):
        score = 0
        next_board = board.clone()
        next_board.play_action(action)
        for i in range(len(self._functions)):
            score += self._parameters[i]*self._functions[i]([board, next_board],player,action)
        return score
    
    def get_default_agent(self):
        return Genetic_1_action_heuristic(self._functions)

    

    

class Genetic_mult_actions_heuristic(Genetic_1_action_heuristic):
    def __init__(self, functions=default_mult_functions, parameters=None):
        super().__init__(functions, parameters)
        
    
    def evaluate(self,init_board,current_board,player,action):
        score = 0

        for i in range(len(self._functions)):
            score += self._parameters[i]*self._functions[i]([init_board,current_board],player,action)
        return score

    def get_default_agent(self):
        return Genetic_mult_actions_heuristic(self._functions)

class Genetic_single_loop_heuristic(Genetic_heuristic):
    def __init__(self, functions=default_single_loop_functions, parameters=None, whole_board_functions=default_board_functions):
        super().__init__(functions, parameters)
        self._whole_board_functions = whole_board_functions
        self._parameters.append([random.uniform(-1,1)]*len(whole_board_functions))

    def evaluate(self,board,player):
        score = 0
        for i in range(9):
            for j in range(9):
                for k in range(len(self._functions)):
                    score += self._parameters[k]*self._functions[k](board,player,i,j)
        # for i in range(len(self._functions),len(self._whole_board_functions)+len(self._functions)):
        #     score += self._parameters[i]*self._whole_board_functions[i-len(self._parameters)]([board,board],player,(0,0))
        return score

    def get_default_agent(self):
        return Genetic_single_loop_heuristic(self._functions,self._whole_board_functions)


