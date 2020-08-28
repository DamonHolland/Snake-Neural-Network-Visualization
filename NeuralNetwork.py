from Neuron import Neuron
from Connection import Connection
import random


class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden_layers, num_outputs, neurons_in_hidden_layers, b_drawn):
        self.num_inputs = num_inputs
        self.num_hidden_layers = num_hidden_layers
        self.num_outputs = num_outputs
        self.neurons_in_hidden_layers = neurons_in_hidden_layers
        self.b_drawn = b_drawn
        self.fitness = 0

        # ---------- Add all neurons to the network ----------
        self.network_neurons = []
        layer = []
        # Add input layers to network
        for i in range(num_inputs):
            layer.append(Neuron(0.0, False, False, self.b_drawn))
        self.network_neurons.append(layer)

        # Add hidden layers to network
        for i in range(num_hidden_layers):
            layer = []
            for j in range(neurons_in_hidden_layers[i]):
                layer.append(Neuron(0.0, True, False, self.b_drawn))
                layer[j].randomize()
            self.network_neurons.append(layer)

        # Add output layers to network
        layer = []
        for i in range(num_outputs):
            layer.append(Neuron(0.0, False, True, self.b_drawn))
            layer[i].randomize()
        self.network_neurons.append(layer)

        # ---------- Add all connections to the network ----------
        self.network_connections = []
        for i in range(len(self.network_neurons) - 1):
            for j in range(len(self.network_neurons[i])):
                for k in range(len(self.network_neurons[i + 1])):
                    self.network_connections.append(Connection(self.network_neurons[i][j],
                                                               self.network_neurons[i + 1][k]))

    def get_output(self, inputs):
        # Set the input neuron values according to given input
        for i in range(self.num_inputs):
            self.network_neurons[0][i].stored_value = inputs[i]

        # Set the stored values of each Neuron by layer
        for i in range(len(self.network_connections)):
            self.network_connections[i].neuron2.stored_value = 0
            self.network_connections[i].neuron2.stored_value += self.network_connections[i].neuron1.get_output() * \
                                                                self.network_connections[i].weight

        # Find the largest output value, and return its index
        largest_value = self.network_neurons[len(self.network_neurons) - 1][0].get_output()
        largest_index = 0
        for i in range(len(self.network_neurons[len(self.network_neurons) - 1])):
            if self.network_neurons[len(self.network_neurons) - 1][i].get_output() > largest_value:
                largest_value = self.network_neurons[len(self.network_neurons) - 1][i].get_output()
                largest_index = i

        return largest_index

    def draw_neurons(self, size, padding_x, padding_y, margin, window):
        for i in range(len(self.network_neurons)):
            for j in range(len(self.network_neurons[i])):
                self.network_neurons[i][j].draw(i, j, size, padding_x, padding_y, margin, window,
                                                len(self.network_neurons[i]), self.num_inputs)

    def draw_connections(self, size, window):
        for i in range(len(self.network_connections)):
            self.network_connections[i].draw(size, window)

    def show_firing_neurons(self, firing_neuron):
        for i in range(len(self.network_neurons[len(self.network_neurons) - 1])):
            if i == firing_neuron:
                self.network_neurons[len(self.network_neurons) - 1][i].look_fire()
            else:
                self.network_neurons[len(self.network_neurons) - 1][i].look_dormant()

    def update_look(self):
        for i in range(len(self.network_connections)):
            self.network_connections[i].update_look()

    def crossover(self, net1, net2):
        for i in range(len(self.network_neurons)):
            for j in range(len(self.network_neurons[i])):
                rand = random.randint(0, 1)
                if rand == 0:
                    self.network_neurons[i][j].bias = net1.network_neurons[i][j].bias
                else:
                    self.network_neurons[i][j].bias = net2.network_neurons[i][j].bias

        for i in range(len(self.network_connections)):
                rand = random.randint(0, 1)
                if rand == 0:
                    self.network_connections[i].weight = net1.network_connections[i].weight
                else:
                    self.network_connections[i].weight = net2.network_connections[i].weight

    def mutate(self, rate):
        for i in range(len(self.network_neurons)):
            for j in range(len(self.network_neurons[i])):
                rand = random.randint(0, rate)
                if rand % rate == 0:
                    self.network_neurons[i][j].randomize()

        for i in range(len(self.network_connections)):
            rand = random.randint(0, rate)
            if rand % rate == 0:
                self.network_connections[i].randomize()