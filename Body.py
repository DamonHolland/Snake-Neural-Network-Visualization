from graphics import *


class Body:
    def __init__(self, x, y, size):
        self.cell_x = x
        self.cell_y = y
        self.size = size
        self.vel = [0, 0]

    def update(self):
        self.cell_x += self.vel[0]
        self.cell_y += self.vel[1]

    def draw(self, window):
        rect = Rectangle(Point((self.cell_x * self.size), (self.cell_y * self.size) + self.size),
                              Point((self.cell_x * self.size) + self.size, (self.cell_y * self.size)))
        rect.setFill('green')
        rect.draw(window)