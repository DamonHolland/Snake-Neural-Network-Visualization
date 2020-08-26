from Snake import Snake
from Apple import Apple
from pynput import keyboard


class Game:
    def __init__(self, grid_size, cell_size, window):
        self.snake = Snake(grid_size / 2, grid_size / 2, cell_size, grid_size, window)
        self.apple = Apple(grid_size, cell_size, window)

    def update(self):
        return self.snake.update(self.apple)

    def on_press(self, key):
        if key == keyboard.Key.up:
            self.snake.up()
        elif key == keyboard.Key.down:
            self.snake.down()
        elif key == keyboard.Key.left:
            self.snake.left()
        elif key == keyboard.Key.right:
            self.snake.right()
