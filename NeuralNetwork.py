from Neuron import Neuron
from Connection import Connection


class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden_layers, num_outputs, neurons_in_hidden_layers):
        self.num_inputs = num_inputs
        self.num_hidden_layers = num_hidden_layers
        self.num_outputs = num_outputs
        self.neurons_in_hidden_layers = neurons_in_hidden_layers

        # ---------- Add all neurons to the network ----------
        self.network_neurons = []
        layer = []
        # Add input layers to network
        for i in range(num_inputs):
            layer.append(Neuron(0.0))
        self.network_neurons.append(layer)

        # Add hidden layers to network
        for i in range(num_hidden_layers):
            layer = []
            for j in range(neurons_in_hidden_layers[i]):
                layer.append(Neuron(0.0))
                layer[j].randomize()
            self.network_neurons.append(layer)

        # Add output layers to network
        layer = []
        for i in range(num_outputs):
            layer.append(Neuron(0.0))
            layer[i].randomize()
        self.network_neurons.append(layer)

        # ---------- Add all connections to the network ----------
        self.network_connections = []
        for i in range(len(self.network_neurons) - 1):
            layer = []
            for j in range(len(self.network_neurons[i])):
                for k in range(len(self.network_neurons[i + 1])):
                    layer.append(Connection(self.network_neurons[i][j], self.network_neurons[i + 1][k]))

    def get_output(self, inputs):
        # Set the input neuron values according to given input
        for i in range(self.num_inputs):
            self.network_neurons[0][i].stored_value = inputs[i]

        # Set the stored values of each Neuron by layer
        for i in range(len(self.network_connections)):
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
