import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class NeuralNetwork:
    def __init__(self, layer_sizes: list[int]):
        self.layer_sizes = layer_sizes
        self.weights = []
        self.biases = []
        
        # Initialize all weights and biases
        rng = np.random.default_rng()
        for i in range(len(self.layer_sizes) - 1):
            self.weights.append(rng.uniform(-0.5, 0.5, size=(self.layer_sizes[i + 1], self.layer_sizes[i])))

        for i in range(1, len(self.layer_sizes)):
            self.biases.append(rng.uniform(-0.5, 0.5, size=(self.layer_sizes[i], 1)))

    def ReLU(self, logits):
        return np.maximum(0, logits)

    def derivative_ReLU(self, logits):
        return logits > 0

    def softmax(self, logits):
        # Subtract by largest number to avoid float overflow in e^logits 
        numerically_stabilized_logits = logits - np.max(logits, axis=0, keepdims=True)

        # Softmax
        exp_logits = np.exp(numerically_stabilized_logits)
        denominator = np.sum(exp_logits, axis=0, keepdims=True)
        return exp_logits / denominator
 
    def forward_propogation(self, X):
        logit_layers = []
        activation_layers = []

        logit = self.weights[0].dot(X) + self.biases[0]
        logit_layers.append(logit)
        activation_layers.append(self.ReLU(logit))

        for i in range(1, len(self.weights)):
            logit = self.weights[i].dot(activation_layers[-1]) + self.biases[i]
            logit_layers.append(logit)

            if i != len(self.weights) - 1:
                activation_layers.append(self.ReLU(logit))

        activation = self.softmax(logit_layers[-1])
        activation_layers.append(activation)

        return logit_layers, activation_layers

    def one_hot_encode(self, Y):
        one_hot_Y = np.zeros((Y.size, self.layer_sizes[0]))
        one_hot_Y[np.arange(Y.size), Y] = 1
        one_hot_Y = one_hot_Y.T
        return one_hot_Y

    def backward_propogation(self, logit_layers, activation_layers, X, Y):
        m = Y.size
        fixed_activation_layers = activation_layers
        fixed_activation_layers.insert(0, X)

        weight_gradients = []
        bias_gradients = []

        pass


    def build_network(self):
        pass

       
new_mlp = NeuralNetwork([8, 16, 32, 2])
X = np.array([
    [0.2],
    [0.5],
    [0.8],
    [0.1],
    [0.4],
    [0.9],
    [0.3],
    [0.7]
])
print(new_mlp.forward_propogation(X))












