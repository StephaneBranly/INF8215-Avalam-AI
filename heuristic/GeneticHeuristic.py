import random
from heuristic.Heuristic import Heuristic
import json

class GeneticHeuristic(Heuristic):
    def __init__(self, functions=None, parameters=None, all_functions=None):
        """
            If functions and parameters are None, the agent will be initialized with random parameters and a sample of functions from all available functions.
        """
        if functions is None:
            nb_functions_to_take = random.randint(1,len(all_functions))
            self._functions = random.sample(all_functions, nb_functions_to_take)
        else:
            self._functions = functions

        if parameters is None:
            self._parameters = [random.uniform(-1,1) for _ in range(len(self._functions))]
        else:
            self._parameters = parameters

        self._all_functions = all_functions

    def evaluate(self):
        pass

    def clone(self):
        raise NotImplementedError
    
    def function_names_to_address(self, function_names):
        return [f for f in self._all_functions if f.__name__ in function_names]

    def interprete_params(self):
        return [f.__name__ for f in self._functions]

    def get_default_agent(self):
        return GeneticHeuristic(self._functions)
    
    def set_parameters(self, parameters):
        self._parameters = parameters
        return self

    def set_functions(self, functions):
        self._functions = functions
    
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

        cl = self.clone()
        cl.set_parameters(new_parameters)
        cl.set_functions(self._functions)
        return cl

    def save_as_json(self, filename, score):
        """Warning: no empty file : it needs to have a array called "gen" """
        with open(filename) as fp:
            listObj = json.load(fp)
        data = {}
        data['score'] = score
        data['parameters'] = self._parameters
        data['functions'] = [f.__name__ for f in self._all_functions if f in self._functions] # non optimal but safe way to save order functions and keep the same order when loading
        listObj["gen"].append(data)
        with open(filename, 'w') as outfile:
            json.dump(listObj, outfile)

    def load_from_json(self, filename, index):
        with open(filename) as fp:
            listObj = json.load(fp)
        self._parameters = listObj["gen"][index]["parameters"]
        if "functions" in listObj["gen"][index]:
            self._functions = [f for f in self._all_functions if f.__name__ in listObj["gen"][index]["functions"]]
