import random
from graphics import *


class Apple:
    def __init__(self, grid_size, cell_size, snake):
        self.grid_size = grid_size
        self.size = cell_size
        self.cell_x = 0
        self.cell_y = 0
        self.move(snake)

    def move(self, snake):
        position_taken = False
        new_x = random.randint(0, self.grid_size - 1)
        new_y = random.randint(0, self.grid_size - 1)
        if new_x == snake.cell_x and new_y == snake.cell_y:
            position_taken = True
        else:
            for i in range(len(snake.body)):
                if new_x == snake.body[i].cell_x and new_y == snake.body[i].cell_y:
                    position_taken = True
        if position_taken:
            self.move(snake)
        else:
            self.cell_x = new_x
            self.cell_y = new_y

    def draw(self, window):
        circle = Circle(Point((self.cell_x * self.size) + self.size / 2,
                                   (self.cell_y * self.size) + self.size / 2), self.size / 2)
        circle.setFill('red')
        circle.draw(window)
