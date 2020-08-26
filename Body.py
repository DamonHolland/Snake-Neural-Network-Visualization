from graphics import *


class Body:

    def __init__(self, x, y, size, window):
        self.window = window
        self.cell_x = x
        self.cell_y = y
        self.size = size
        self.rect = Rectangle(Point((self.cell_x * self.size), (self.cell_y * self.size) + self.size),
                              Point((self.cell_x * self.size) + self.size, (self.cell_y * self.size)))
        self.vel = [0, 0]
        self.draw()

    def draw(self):
        self.rect.setFill('green')
        self.rect.draw(self.window)

    def update(self):
        self.cell_x += self.vel[0]
        self.cell_y += self.vel[1]
        self.rect.move(self.vel[0] * self.size, self.vel[1] * self.size)
