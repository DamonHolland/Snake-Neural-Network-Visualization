from graphics import *
from Body import Body
import random


class Snake:
    def __init__(self, size, grid_size, window, neural_net):
        self.neural_net = neural_net
        self.window = window
        self.grid_size = grid_size
        self.cell_x = random.randint(0, grid_size - 1)
        self.cell_y = random.randint(0, grid_size - 1)
        self.size = size
        self.vel = [0, 0]
        self.body = []
        self.is_alive = True
        self.max_moves = 100
        self.move_count = 0

        if self.neural_net.b_drawn:
            self.rect = Rectangle(Point((self.cell_x * self.size), (self.cell_y * self.size) + self.size),
                                  Point((self.cell_x * self.size) + self.size, (self.cell_y * self.size)))
            self.rect.setFill('green')
            self.rect.setOutline('green')
            self.rect.draw(window)

    def update(self, apple):
        self.move_count += 1

        self.cell_x += self.vel[0]
        self.cell_y += self.vel[1]
        if self.neural_net.b_drawn:
            self.rect.move(self.vel[0] * self.size, self.vel[1] * self.size)

        if self.cell_x == apple.cell_x and self.cell_y == apple.cell_y:
            apple.move(self)
            self.grow()
            self.move_count = 0

        for i in range(len(self.body)):
            self.body[i].update()
            if self.cell_x == self.body[i].cell_x and self.cell_y == self.body[i].cell_y:
                self.is_alive = False
            if i == 0:
                self.body[i].vel = [self.cell_x - self.body[i].cell_x, self.cell_y - self.body[i].cell_y]
            else:
                self.body[i].vel = [self.body[i - 1].cell_x - self.body[i].cell_x,
                                    self.body[i - 1].cell_y - self.body[i].cell_y]

        if self.cell_x < 0 or self.cell_x >= self.grid_size or self.cell_y < 0 or self.cell_y >= self.grid_size\
            or self.move_count > self.max_moves:
            self.is_alive = False

        if not self.is_alive:
            self.neural_net.fitness = 1 + (len(self.body) * 100) -\
                                      (self.grid_size - (abs(self.cell_x - apple.cell_x) +
                                                         abs(self.cell_y - apple.cell_y))) +\
                                      (self.move_count / self.max_moves)

        # --------------- Neural Network ---------------

        # Find The closest cells in each direction / Normalize Input
        closest_up = self.grid_size
        closest_down = self.grid_size
        closest_left = self.grid_size
        closest_right = self.grid_size
        for i in range(len(self.body)):
            if self.cell_x == self.body[i].cell_x:
                if self.cell_y < self.body[i].cell_y:
                    if self.body[i].cell_y - self.cell_y < closest_down:
                        closest_down = self.body[i].cell_y - self.cell_y
                else:
                    if self.cell_y - self.body[i].cell_y < closest_up:
                        closest_up = self.cell_y - self.body[i].cell_y
            elif self.cell_y == self.body[i].cell_y:
                if self.cell_x > self.body[i].cell_x:
                    if self.cell_x - self.body[i].cell_x < closest_left:
                        closest_left = self.cell_x - self.body[i].cell_x
                else:
                    if self.body[i].cell_x - self.cell_x < closest_right:
                        closest_right = self.body[i].cell_x - self.cell_x
        if closest_up == self.grid_size:
            closest_up = self.cell_y
        if closest_down == self.grid_size:
            closest_down = self.grid_size - self.cell_y
        if closest_right == self.grid_size:
            closest_right = self.grid_size - self.cell_x
        if closest_left == self.grid_size:
            closest_left = self.cell_x
        closest_up = (closest_up - (self.grid_size / 2)) / (self.grid_size / 2)
        closest_down = (closest_down - (self.grid_size / 2)) / (self.grid_size / 2)
        closest_left = (closest_left - (self.grid_size / 2)) / (self.grid_size / 2)
        closest_right = (closest_right - (self.grid_size / 2)) / (self.grid_size / 2)

        # Find The x and y distance to the apple, Normalize input
        apple_diff_x = abs(self.cell_x - apple.cell_x)
        apple_diff_y = abs(self.cell_y - apple.cell_y)
        apple_diff_x = (apple_diff_x - (self.grid_size / 2)) / (self.grid_size / 2)
        apple_diff_y = (apple_diff_y - (self.grid_size / 2)) / (self.grid_size / 2)

        output = self.neural_net.get_output([closest_up, closest_down, closest_left, closest_right,
                                             apple_diff_x, apple_diff_y])

        if self.neural_net.b_drawn:
            self.neural_net.show_firing_neurons(output)

        if output == 0:
            self.up()
        elif output == 1:
            self.down()
        elif output == 2:
            self.left()
        elif output == 3:
            self.right()

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
            new_body = Body(self.cell_x - self.vel[0], self.cell_y - self.vel[1], self.size, self.window,
                            self.neural_net.b_drawn)
        else:
            new_body = Body(self.body[len(self.body) - 1].cell_x,
                            self.body[len(self.body) - 1].cell_y,
                            self.size, self.window, self.neural_net.b_drawn)
        self.body.append(new_body)
