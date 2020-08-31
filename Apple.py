import random
from graphics import *


class Apple:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.size = cell_size
        self.cell_x = random.randint(0, grid_size - 1)
        self.cell_y = random.randint(0, grid_size - 1)

    def move(self, snake):
        position_found = False
        new_x = new_y = 0
        while not position_found:
            position_taken = False
            new_x = random.randint(0, self.grid_size - 1)
            new_y = random.randint(0, self.grid_size - 1)
            if new_x == snake.cell_x and new_y == snake.cell_y:
                position_taken = True
            else:
                if len(snake.body) != 0:
                    for cell in snake.body[:]:
                        if new_x == cell.cell_x and new_y == cell.cell_y:
                            position_taken = True
            if not position_taken:
                position_found = True
        self.cell_x = new_x
        self.cell_y = new_y

    def draw(self, window):
        circle = Circle(Point((self.cell_x * self.size) + self.size / 2,
                                   (self.cell_y * self.size) + self.size / 2), self.size / 2)
        circle.setFill('red')
        circle.draw(window)
