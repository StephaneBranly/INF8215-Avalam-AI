import json
from heuristic.NN.neural_network import NN
from heuristic.GeneticHeuristic import GeneticHeuristic
from heuristic.observation_function import *
import numpy as np

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
class NNGeneticHeuristic(GeneticHeuristic):
    def __init__(self, functions=None,parameters=None,all_functions=all_board_evaluation_functions):
        self.core = NN([len(all_functions), 10, 1]) #tu peux edit la compo des couche voir meme passer en argument stv
        super().__init__(functions, parameters, all_functions)
    
    def evaluate(self,board,player,action):
        return self.core.predict([1 for i in range(len(self._functions))]) # donne en arg les valeurs des fonctions d'observations (ici j'ai mis un truc au pif)
    
    def crossover(self, other):
        c1,c2 = self.core.crossover(other.core)
        return NNGeneticHeuristic(self._functions,c1), NNGeneticHeuristic(self._functions,c2)

    def mutate(self,mutation_rate):
        self.core.mutate(mutation_rate)
        return self
    
    def clone(self):
        return NNGeneticHeuristic(self._functions,self.core.clone())


    def get_default_agent(self):
        return NNGeneticHeuristic(self._functions)
    
    def save_as_json(self, filename, score):

        with open(filename) as fp:
            listObj = json.load(fp)

        data = {}
        data['score'] = score

        data['functions'] = [f.__name__ for f in self._all_functions if f in self._functions] # non optimal but safe way to save order functions and keep the same order when loading

        # sauvegarde du core (NN)
        core = {}
        w  = [a.tolist() for a in self.core.weights]
        b  = [a.tolist() for a in self.core.biases]
        core['name'] = self.core.name
        core['score'] = score
        core['weights'] = w
        core['biases'] = b
        core['layers'] = self.core.layers

        data['core'] = core

        listObj["gen"].append(data)
        with open(filename, 'w') as outfile:
            json.dump(listObj, outfile)

    def load_from_json(self, filename, index):
        with open(filename) as fp:
            listObj = json.load(fp)
        if "functions" in listObj["gen"][index]:
            self._functions = [f for f in self._all_functions if f.__name__ in listObj["gen"][index]["functions"]]

        self.core.name = listObj["gen"][index]["core"]["name"]
        self.core.weights = [np.array(a) for a in listObj["gen"][index]["core"]["weights"]]
        self.core.biases = [np.array(a) for a in listObj["gen"][index]["core"]["biases"]]
        self.core.layers = listObj["gen"][index]["core"]["layers"]

