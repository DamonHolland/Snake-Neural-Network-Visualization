import random
from graphics import *
import copy
import math


class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden_layers, num_outputs, neurons_in_hidden_layers):
        self.fitness = 0

        # ---------- Add all neuron biases to the network ----------
        self.network_neuron_biases = []
        layer = []
        # Add input biases to network (0)
        for i in range(num_inputs):
            layer.append(0)
        self.network_neuron_biases.append(layer)

        # Add hidden layer biases to network (Random)
        for i in range(num_hidden_layers):
            layer = []
            for j in range(neurons_in_hidden_layers[i]):
                layer.append(random.randint(-100, 100) / 100.0)
            self.network_neuron_biases.append(layer)

        # Add output layer biases to network (0)
        layer = []
        for i in range(num_outputs):
            layer.append(0)
        self.network_neuron_biases.append(layer)

        # ---------- Add all connection weights to the network (Random)----------
        self.network_connection_weights = []
        for i in range(len(self.network_neuron_biases) - 1):
            for j in range(len(self.network_neuron_biases[i])):
                for k in range(len(self.network_neuron_biases[i + 1])):
                    self.network_connection_weights.append(random.randint(-100, 100) / 100.0)

    def get_output(self, inputs):
        # Set the input neuron values according to given input
        node_outputs = [inputs]

        # Set the stored values of each Neuron by layer
        current_weight = 0
        for i in range(len(self.network_neuron_biases) - 1):
            layer = []
            for j in range(len(self.network_neuron_biases[i + 1])):
                output_value = self.network_neuron_biases[i + 1][j]
                for k in range(len(self.network_neuron_biases[i])):
                    output_value += node_outputs[i][k] * self.network_connection_weights[current_weight]
                    current_weight += 1
                if i != 0 or i != range(len(self.network_neuron_biases) - 1):
                    output_value = 1 / (1 + math.exp(-output_value))
                layer.append(output_value)
            node_outputs.append(layer)

        # Find the largest output value, and return its index
        return node_outputs[len(node_outputs) - 1].index(max(node_outputs[len(node_outputs) - 1]))

    def crossover(self, net1, net2):
        # Set each node bias to the corresponding parent, each bias chosen with a random parent
        for i in range(len(self.network_neuron_biases)):
            for j in range(len(self.network_neuron_biases[i])):
                rand = random.randint(0, 1)
                if rand == 0:
                    self.network_neuron_biases[i][j] = net1.network_neuron_biases[i][j]
                else:
                    self.network_neuron_biases[i][j] = net2.network_neuron_biases[i][j]

        # Set each connection weight to the corresponding parent, each connection chosen with a random parent
        for i in range(len(self.network_connection_weights)):
                rand = random.randint(0, 1)
                if rand == 0:
                    self.network_connection_weights[i] = net1.network_connection_weights[i]
                else:
                    self.network_connection_weights[i] = net2.network_connection_weights[i]

    def mutate(self, rate):
        # Mutate each neuron bias at a specified rate
        for i in range(len(self.network_neuron_biases)):
            if i != 0 and i != len(self.network_neuron_biases) - 1:
                for j in range(len(self.network_neuron_biases[i])):
                    rand = random.randint(0, rate)
                    if rand % rate == 0:
                        self.network_neuron_biases[i][j] = random.randint(-100, 100) / 100.0

        # Mutate each neuron bias at a specified rate
        for i in range(len(self.network_connection_weights)):
            if i != 0 and i != len(self.network_connection_weights) - 1:
                    rand = random.randint(0, rate)
                    if rand % rate == 0:
                        self.network_connection_weights[i] = random.randint(-100, 100) / 100.0

    def draw(self, window, inputs, neuron_size, neuron_padding_x, neuron_padding_y, top_padding, most_neurons):
        # First, get an array of outputs that will be used to show neurons
        node_outputs = [inputs]

        # Set the stored values of each Neuron by layer
        current_weight = 0
        for i in range(len(self.network_neuron_biases) - 1):
            layer = []
            for j in range(len(self.network_neuron_biases[i + 1])):
                output_value = self.network_neuron_biases[i + 1][j]
                for k in range(len(self.network_neuron_biases[i])):
                    output_value += node_outputs[i][k] * self.network_connection_weights[current_weight]
                    current_weight += 1
                if i != 0 or i != range(len(self.network_neuron_biases) - 1):
                    output_value = 1 / (1 + math.exp(-output_value))
                layer.append(output_value)
            node_outputs.append(layer)

        # Find the largest output value, and store its index
        largest_value = node_outputs[len(node_outputs) - 1][0]
        largest_index = 0
        for i in range(len(node_outputs[len(node_outputs) - 1])):
            if node_outputs[len(node_outputs) - 1][i] > largest_value:
                largest_value = node_outputs[len(self.network_neuron_biases) - 1][i]
                largest_index = i

        # Create the neurons based on their output, save them so you can draw after connections (layering)
        neurons_positions = []
        saved_neurons = []
        for i in range(len(node_outputs)):
            neuron_pos_layer = []
            for j in range(len(node_outputs[i])):
                mid_x = i * (neuron_size + neuron_padding_x) + (neuron_padding_x / 2) + neuron_size
                mid_y = j * (neuron_size + neuron_padding_y) + (neuron_padding_y / 2) + top_padding + neuron_size +\
                        ((most_neurons - len(node_outputs[i])) /  2) * (neuron_size + neuron_padding_y)
                neuron_pos_layer.append([mid_x, mid_y])
                neuron = Circle(Point(mid_x, mid_y), neuron_size / 2)
                if i != len(node_outputs) - 1:
                    rgb_blue = int((node_outputs[i][j] * 127.5) + 127.5)
                    neuron.setFill(color_rgb(255 - rgb_blue, 255 - rgb_blue, 255))
                else:
                    if j == largest_index:
                        neuron.setFill('blue')
                    else:
                        neuron.setFill('white')
                saved_neurons.append(neuron)
            neurons_positions.append(neuron_pos_layer)

        # Now draw connections between neurons based on their weights
        current_weight = 0
        for i in range(len(neurons_positions) - 1):
            for j in range(len(neurons_positions[i])):
                for k in range(len(neurons_positions[i + 1])):
                    connection = Line(Point(neurons_positions[i][j][0] + neuron_size / 2, neurons_positions[i][j][1]),
                                      Point(neurons_positions[i + 1][k][0] - neuron_size / 2,
                                            neurons_positions[i + 1][k][1]))
                    if self.network_connection_weights[current_weight] >= 0:
                        connection.setFill('blue')
                    else:
                        connection.setFill('red')
                    connection.draw(window)
                    current_weight += 1

        # Now draw the neurons on top of connections
        for i in range(len(saved_neurons)):
            saved_neurons[i].draw(window)
