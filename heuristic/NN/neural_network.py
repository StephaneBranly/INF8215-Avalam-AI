import numpy as np
import json

class NN:

    def __init__(self, layers, name=""):
        self.name = name
        self.layers = layers
        self.weights = []
        self.biases = []
        for i in range(len(layers)-1):
            self.biases.append(np.random.randn(layers[i+1], 1))
            self.weights.append(np.random.randn(layers[i], layers[i+1]))        

    def sigmoid(self, z):
        return 1.0/(1.0+np.exp(-z))

    def print(self):
        print(self.weights)
        print(self.biases)

    def predict(self, x):
        for i in range(len(self.weights)):
            x = self.sigmoid(np.dot(x,self.weights[i])+self.biases[i].T)

        return x[0]
    
    def mutate(self, rate=0.01):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    if np.random.rand() < rate:
                        self.weights[i][j][k] = np.random.randn()
        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                for k in range(len(self.biases[i][j])):
                    if np.random.rand() < rate:
                        self.biases[i][j][k] = np.random.randn()

    def crossover(self, other):
        child1 = NN(self.layers)
        child2 = NN(self.layers)

        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    if np.random.rand() < 0.5:
                        child1.weights[i][j][k] = self.weights[i][j][k]
                        child2.weights[i][j][k] = other.weights[i][j][k]
                    else:
                        child1.weights[i][j][k] = other.weights[i][j][k]
                        child2.weights[i][j][k] = self.weights[i][j][k]
        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                for k in range(len(self.biases[i][j])):
                    if np.random.rand() < 0.5:
                        child1.biases[i][j][k] = self.biases[i][j][k]
                        child2.biases[i][j][k] = other.biases[i][j][k]
                    else:
                        child1.biases[i][j][k] = other.biases[i][j][k]
                        child2.biases[i][j][k] = self.biases[i][j][k]
        return child1, child2

    def save_as_json(self, filename, score):
        """Warning: no empty file : it needs to have a array called "gen" """
        with open(filename) as fp:
            listObj = json.load(fp)
        data = {}
        w  = [a.tolist() for a in self.weights]
        b  = [a.tolist() for a in self.biases]
        data['name'] = self.name
        data['score'] = score
        data['weights'] = w
        data['biases'] = b
        data['layers'] = self.layers
        listObj["gen"].append(data)
        with open(filename, 'w') as outfile:
            json.dump(listObj, outfile)

    def load_from_json(self, filename, index):
        with open(filename) as fp:
            listObj = json.load(fp)
        self.name = listObj["gen"][index]["name"]
        self.weights = [np.array(a) for a in listObj["gen"][index]["weights"]]
        self.biases = [np.array(a) for a in listObj["gen"][index]["biases"]]
        self.layers = listObj["gen"][index]["layers"]
    
    def clone(self):
        clone = NN(self.layers)
        clone.weights = self.weights
        clone.biases = self.biases
        return clone