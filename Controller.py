from Game import Game
from NeuralNetwork import NeuralNetwork
from graphics import *


class Controller:
    def __init__(self, num_games, grid_size, cell_size, window, num_inputs,
                 num_hidden_layers, num_outputs, neurons_in_hidden_layers,
                 neuron_size, neuron_padding_x, neuron_padding_y, top_padding, window_nn):
        self.num_games = num_games
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window = window
        self.num_inputs = num_inputs
        self.num_hidden_layers = num_hidden_layers
        self.num_outputs = num_outputs
        self.neurons_in_hidden_layers = neurons_in_hidden_layers
        self.neuron_size = neuron_size
        self.neuron_padding_x = neuron_padding_x
        self.neuron_padding_y = neuron_padding_y
        self.top_padding = top_padding
        self.window_nn = window_nn
        self.generation = 1
        self.text = Text(Point(100, 20), "Generation: " + str(self.generation))
        self.text.setTextColor('white')
        self.text.setSize(20)
        self.draw_info()

        self.simulation_running = True
        self.games = []
        for i in range(num_games):
            if i == 0:
                net = NeuralNetwork(num_inputs, num_hidden_layers, num_outputs, neurons_in_hidden_layers, True)
                net.draw_neurons(neuron_size, neuron_padding_x, neuron_padding_y, top_padding, window_nn)
                net.draw_connections(neuron_size, window_nn)
                net.update_look()
            else:
                net = NeuralNetwork(num_inputs, num_hidden_layers, num_outputs, neurons_in_hidden_layers, False)
            self.games.append(Game(grid_size, cell_size, window, net))

    def update(self):
        b_simulation_finished = False
        for i in range(self.num_games):
            if self.games[i].is_running:
                self.games[i].update()

        if not self.games[0].is_running:
            b_any_game_running = True
            while b_any_game_running:
                b_any_game_running = False
                for j in range(self.num_games):
                    if self.games[j].is_running:
                        b_any_game_running = True
                        self.games[j].update()
            b_simulation_finished = True

        if b_simulation_finished:
            self.generation += 1
            for item in self.window_nn.items[:]:
                item.undraw()
            for item in self.window.items[:]:
                item.undraw()
            self.games = []
            self.text.setText("Generation: " + str(self.generation))
            self.draw_info()
            for i in range(self.num_games):
                if i == 0:
                    net = NeuralNetwork(self.num_inputs, self.num_hidden_layers, self.num_outputs,
                                        self.neurons_in_hidden_layers, True)
                    net.draw_neurons(self.neuron_size, self.neuron_padding_x, self.neuron_padding_y,
                                     self.top_padding, self.window_nn)
                    net.draw_connections(self.neuron_size, self.window_nn)
                    net.update_look()
                else:
                    net = NeuralNetwork(self.num_inputs, self.num_hidden_layers, self.num_outputs,
                                        self.neurons_in_hidden_layers, False)
                self.games.append(Game(self.grid_size, self.cell_size, self.window, net))

    def draw_info(self):
        self.text.draw(self.window_nn)
