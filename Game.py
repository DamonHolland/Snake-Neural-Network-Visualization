from Snake import Snake
from Apple import Apple


class Game:
    def __init__(self, grid_size, cell_size, window, neural_net):
        self.is_running = True
        self.snake = Snake(cell_size, grid_size, window, neural_net)
        self.apple = Apple(grid_size, cell_size, window, neural_net.b_drawn)

    def update(self):
        self.is_running = self.snake.update(self.apple)
