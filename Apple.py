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
        while True:
            intersect = False
            self.cell_x = random.randint(0, self.grid_size - 1)
            self.cell_y = random.randint(0, self.grid_size - 1)
            for i in range(len(snake.body)):
                if self.cell_x == snake.body[i].cell_x and self.cell_y == snake.body[i].cell_y:
                    intersect = True
            if not intersect:
                break

    def draw(self, window):
        circle = Circle(Point((self.cell_x * self.size) + self.size / 2,
                              (self.cell_y * self.size) + self.size / 2), self.size / 2)
        circle.setFill('red')
        circle.draw(window)
