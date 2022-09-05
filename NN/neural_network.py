import numpy as np

class NN:

    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        for i in range(len(layers)-1):
            self.biases.append(np.random.randn(layers[i+1], 1)*5)
            self.weights.append(np.random.randn(layers[i+1], layers[i])*5)

            
    def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases
        

    def sigmoid(self, z):
        return 1.0/(1.0+np.exp(-z))

    def print(self):
        print(self.weights)
        print(self.biases)

    def predict(self, x):
        for i in range(len(self.weights)):
            print(x.shape, self.weights[i].shape, self.biases[i].shape)
            x = self.sigmoid(np.dot(self.weights[i], x)+self.biases[i])
        return (np.argmax(x), np.max(x))

