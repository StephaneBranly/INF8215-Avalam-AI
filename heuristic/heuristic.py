from .observation_function import finish_tower, isolate_tower, use_token, cover_token
import random
import json

class Heuristic:
    def __init__(self):
        pass

    def evaluate(self,board,player,action):
        raise NotImplementedError

    def __call__(self,board,player,action):
        return self.evaluate(board,player,action)


class Genetic_1_action_heuristique(Heuristic):
    def __init__(self):
        self.parameters = [random.uniform(-1,1) for parameters in range(5)]



    def evaluate(self,board,player,action):
        score = 0
        score += self.parameters[0]*finish_tower(board,player,action)
        score += self.parameters[1]*isolate_tower(board,player,action)
        score += self.parameters[2]*isolate_tower(board,-player,action)
        score += self.parameters[3]*use_token(board,player,action)
        score += self.parameters[4]*cover_token(board,player,action)
        return score
    
    def set_parameters(self,parameters):
        self.parameters = parameters
    
    def get_parameters(self):
        return self.parameters

    def mutate(self,mutation_rate):
        for i in range(len(self.parameters)):
            if random.random() < mutation_rate:
                self.parameters[i] += random.uniform(-1,1)

    def crossover(self,other):
        new_parameters = []
        for i in range(len(self.parameters)):
            if random.random() < 0.5:
                new_parameters.append(self.parameters[i])
            else:
                new_parameters.append(other.parameters[i])
        return Genetic_1_action_heuristique(new_parameters)

    def save_as_json(self, filename, score):
        """Warning: no empty file : it needs to have a array called "gen" """
        with open(filename) as fp:
            listObj = json.load(fp)
        data = {}
        data['score'] = score
        data['parameters'] = self.parameters
        listObj["gen"].append(data)
        with open(filename, 'w') as outfile:
            json.dump(listObj, outfile)

    def load_from_json(self, filename, index):
        with open(filename) as fp:
            listObj = json.load(fp)
        self.parameters = listObj["gen"][index]["parameters"]
