from Game import Game
from NeuralNetwork import NeuralNetwork


class Controller:
    def __init__(self, num_games, grid_size, cell_size, window, num_inputs,
                 num_hidden_layers, num_outputs, neurons_in_hidden_layers,
                 neuron_size, neuron_padding_x, neuron_padding_y, top_padding, window_nn):
        self.simulation_running = True
        self.num_games = num_games
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
            self.simulation_running = False
