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

    def Tanh(self, logits):
        return np.tanh(logits)
 
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

        activation = self.Tanh(logit_layers[-1])
        activation_layers.append(activation)

        return logit_layers, activation_layers

    def get_params(self):
        chromosome = []

        for i in self.weights:
            flattened_array = i.flatten()
            chromosome.append(flattened_array)

        for i in self.biases:
            flattened_array = i.flatten()
            chromosome.append(flattened_array)

        return np.concatenate(chromosome)

    def set_params(self, chromosome):
        prev_layer_size = 0
        prev_bias = len(chromosome) - np.sum(self.layer_sizes[1:])

        new_weights = []
        new_biases = []

        for y in range(len(self.layer_sizes) - 1):
            cur_layer_size = prev_layer_size + (self.layer_sizes[y] * self.layer_sizes[y + 1])
            cur_bias = prev_bias + self.layer_sizes[y + 1]

            weights = chromosome[prev_layer_size:cur_layer_size]
            biases = chromosome[prev_bias:cur_bias]

            new_weights.append(np.reshape(weights, (self.layer_sizes[y + 1], self.layer_sizes[y])))
            new_biases.append(np.reshape(biases, (self.layer_sizes[y + 1], 1)))

            prev_layer_size = prev_layer_size + (self.layer_sizes[y] * self.layer_sizes[y + 1])
            prev_bias = prev_bias + self.layer_sizes[y + 1]        

        self.weights = new_weights
        self.biases = new_biases
        

       
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

new_mlp.forward_propogation(X)
chromosome = new_mlp.get_params()
new_mlp.set_params(chromosome)
















