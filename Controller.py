from Game import Game
from NeuralNetwork import NeuralNetwork
from graphics import *
import random


def sort_net(net):
    return net.fitness


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
        self.fitness_text = Text(Point(280, 50), "Highest Fitness: 0")
        self.fitness_text.setTextColor('white')
        self.fitness_text.setSize(20)

        self.draw_info()
        self.best_networks = []
        self.max_best_networks = 10
        self.num_crossovers = 50
        self.mutation_rate = 50

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
            for i in range(self.num_games):
                if len(self.best_networks) < self.max_best_networks:
                    self.best_networks.append(self.games[i].snake.neural_net)
                else:
                    self.best_networks.sort(key = sort_net, reverse=True)
                    if self.games[i].snake.neural_net.fitness > self.best_networks[self.max_best_networks - 1].fitness:
                        self.best_networks[self.max_best_networks - 1] = self.games[i].snake.neural_net

            self.generation += 1
            for item in self.window_nn.items[:]:
                item.undraw()
            for item in self.window.items[:]:
                item.undraw()
            self.games = []
            self.text.setText("Generation: " + str(self.generation))
            self.fitness_text.setText("Highest Fitness: " + str(self.best_networks[0].fitness))
            self.draw_info()
            for i in range(self.num_games):
                if i == 0:
                    net = NeuralNetwork(self.num_inputs, self.num_hidden_layers, self.num_outputs,
                                        self.neurons_in_hidden_layers, True)
                    net.crossover(self.best_networks[0], self.best_networks[0])
                    net.draw_neurons(self.neuron_size, self.neuron_padding_x, self.neuron_padding_y,
                                     self.top_padding, self.window_nn)
                    net.draw_connections(self.neuron_size, self.window_nn)
                    net.update_look()
                elif i <= len(self.best_networks) - 1:
                    net = NeuralNetwork(self.num_inputs, self.num_hidden_layers, self.num_outputs,
                                        self.neurons_in_hidden_layers, False)
                    net.crossover(self.best_networks[i], self.best_networks[i])
                elif i <= self.num_crossovers + len(self.best_networks) - 1:
                    net = NeuralNetwork(self.num_inputs, self.num_hidden_layers, self.num_outputs,
                                        self.neurons_in_hidden_layers, False)
                    rand1 = random.randint(0, self.max_best_networks - 1)
                    rand2 = random.randint(0, self.max_best_networks - 1)
                    while rand2 == rand1:
                        rand2 = random.randint(0, self.max_best_networks - 1)
                    net.crossover(self.best_networks[rand1], self.best_networks[rand2])
                    net.mutate(self.mutation_rate)
                else:
                    net = NeuralNetwork(self.num_inputs, self.num_hidden_layers, self.num_outputs,
                                        self.neurons_in_hidden_layers, False)
                self.games.append(Game(self.grid_size, self.cell_size, self.window, net))

    def draw_info(self):
        self.text.draw(self.window_nn)
        self.fitness_text.draw(self.window_nn)

