# Neural Network
#from sklearn.utils.extmath import softmax
from datetime import datetime
import numpy as np, os

class NeuralNetwork:

    ''' --- docstring for NeuralNetwork ---

    '''

    def __init__(self, structure):

        self.structure = structure
        self.num_layers = len(structure)

        self.build_weights()
        self.build_bias()

        self.activation = [sigmoid] * (self.num_layers - 1)

    def build_weights(self):
        self.weights = [np.random.random_sample((self.structure[i+1], self.structure[i])) * 2 - 1 for i in range(self.num_layers - 1)]

    def build_bias(self):
        self.bias = [np.random.random_sample((self.structure[i], 1)) * 2 - 1 for i in range(1,self.num_layers)]

    def predict(self, input_):

        for i in range(self.num_layers - 1):

            if i == 0:
                node_in = input_ # initial input
            else:
                node_in = h # output of the last layer

            z = self.weights[i].dot(node_in) + self.bias[i] # raw output of layer (no activation function)
            h = self.activation[i](z) # final output of layer
        
        print(h)

        return h

    def mutate(self, prob):

        mutate_val = lambda val, prob: val + np.random.normal(0, .1) if np.random.random() < prob else val

        vfunc = np.vectorize(mutate_val)

        self.weights = [vfunc(W,prob) for W in self.weights]
        self.bias = [vfunc(b,prob) for b in self.bias]

    def clone(self):

        clone = NeuralNetwork(self.structure)
        clone.weights = self.weights[:]
        clone.bias = self.bias[:]
        clone.activation = self.activation

        return clone
    
    def save(self, env):

        time = str(datetime.now()).split('.')[0]

        if not os.path.isdir('saved models'):
            os.mkdir('saved models')

        np.save('saved models/{} - weights'.format(time), self.weights)
        np.save('saved models/{} - bias'.format(time), self.bias)
        np.save('saved models/{} - info'.format(time), env.get_clone_info())


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return x if x > 0 else 0

def leaky_relu(x):
    return x if x >= 0 else x * .01

def parametric_relu(x):
    pass

def swish(x):
    # not sure ...
    return x * sigmoid(x)




