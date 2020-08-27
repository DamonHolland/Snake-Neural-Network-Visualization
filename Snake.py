from graphics import *
from Body import Body


class Snake:

    def __init__(self, x, y, size, grid_size, window):
        self.window = window
        self.grid_size = grid_size
        self.cell_x = x
        self.cell_y = y
        self.size = size
        self.rect = Rectangle(Point((self.cell_x * self.size), (self.cell_y * self.size) + self.size),
                              Point((self.cell_x * self.size) + self.size, (self.cell_y * self.size)))
        self.vel = [0, 0]
        self.body = []
        self.is_alive = True
        self.draw()

    def draw(self):
        self.rect.setFill('green')
        self.rect.setOutline('green')
        self.rect.draw(self.window)

    def update(self, apple):
        self.cell_x += self.vel[0]
        self.cell_y += self.vel[1]
        self.rect.move(self.vel[0] * self.size, self.vel[1] * self.size)

        if self.cell_x == apple.cell_x and self.cell_y == apple.cell_y:
            apple.move(self)
            self.grow()

        for i in range(len(self.body)):
            self.body[i].update()
            if self.cell_x == self.body[i].cell_x and self.cell_y == self.body[i].cell_y:
                print("Final Score: " + str(len(self.body)))
                self.is_alive = False
            if i == 0:
                self.body[i].vel = [self.cell_x - self.body[i].cell_x, self.cell_y - self.body[i].cell_y]
            else:
                self.body[i].vel = [self.body[i - 1].cell_x - self.body[i].cell_x,
                                    self.body[i - 1].cell_y - self.body[i].cell_y]

        if self.cell_x < 0 or self.cell_x >= self.grid_size or self.cell_y < 0 or self.cell_y >= self.grid_size:
            print("Final Score: " + str(len(self.body)))
            self.is_alive = False

        return self.is_alive

    def up(self):
        if len(self.body) == 0 or self.cell_y != self.body[0].cell_y + 1:
            self.vel = [0, -1]

    def down(self):
        if len(self.body) == 0 or self.cell_y != self.body[0].cell_y - 1:
            self.vel = [0, 1]

    def left(self):
        if len(self.body) == 0 or self.cell_x != self.body[0].cell_x + 1:
            self.vel = [-1, 0]

    def right(self):
        if len(self.body) == 0 or self.cell_x != self.body[0].cell_x - 1:
            self.vel = [1, 0]

    def grow(self):
        if len(self.body) == 0:
            new_body = Body(self.cell_x - self.vel[0], self.cell_y - self.vel[1], self.size, self.window)
        else:
            new_body = Body(self.body[len(self.body) - 1].cell_x,
                            self.body[len(self.body) - 1].cell_y,
                            self.size, self.window)
        self.body.append(new_body)
