from Snake import Snake
from Apple import Apple


class Game:
    def __init__(self, grid_size, cell_size, window, neural_net):
        self.snake = Snake(grid_size / 2, grid_size / 2, cell_size, grid_size, window, neural_net)
        self.apple = Apple(grid_size, cell_size, window)

    def update(self):
        return self.snake.update(self.apple)
