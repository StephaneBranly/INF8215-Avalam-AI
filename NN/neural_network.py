import numpy as np

class NN:

    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        for i in range(len(layers)-1):
            self.biases.append(np.random.randn(layers[i+1], 1))
            self.weights.append(np.random.randn(layers[i], layers[i+1]))


    """def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases"""
        

    def sigmoid(self, z):
        return 1.0/(1.0+np.exp(-z))

    def print(self):
        print(self.weights)
        print(self.biases)

    def predict(self, x):
        for i in range(len(self.weights)):
            x = self.sigmoid(np.dot(x,self.weights[i])+self.biases[i].T)

        return (np.argmax(x), np.max(x))
    
    def mutate(self, rate):
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
        child = NN(self.layers)
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    if np.random.rand() < 0.5:
                        child.weights[i][j][k] = self.weights[i][j][k]
                    else:
                        child.weights[i][j][k] = other.weights[i][j][k]
        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                for k in range(len(self.biases[i][j])):
                    if np.random.rand() < 0.5:
                        child.biases[i][j][k] = self.biases[i][j][k]
                    else:
                        child.biases[i][j][k] = other.biases[i][j][k]
        return child


