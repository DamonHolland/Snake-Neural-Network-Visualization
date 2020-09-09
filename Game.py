from Snake import Snake
from Apple import Apple


class Game:
    def __init__(self, grid_size, cell_size, neural_net):
        self.is_running = True
        self.snake = Snake(cell_size, grid_size, neural_net)
        self.apple = Apple(grid_size, cell_size, self.snake)

    def update(self):
        self.is_running = self.snake.update(self.apple)

    def draw(self, window, window_nn, neuron_size, neuron_padding_x, neuron_padding_y, top_padding, most_neurons):
        self.snake.draw(window)
        self.apple.draw(window)
        self.snake.neural_net.draw(window_nn, self.snake.get_nn_input(self.apple), neuron_size, neuron_padding_x,
                                   neuron_padding_y, top_padding, most_neurons)
