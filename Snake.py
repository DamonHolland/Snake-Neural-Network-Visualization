from graphics import *
from Body import Body
import random


class Snake:
    def __init__(self, size, grid_size, neural_net):
        self.neural_net = neural_net
        self.grid_size = grid_size
        self.cell_x = random.randint(0, grid_size - 1)
        self.cell_y = random.randint(0, grid_size - 1)
        self.size = size
        self.vel = [0, 0]
        self.body = []
        self.is_alive = True
        self.max_moves = 100
        self.move_count = 0
        self.fitness = 0

    def update(self, apple):
        self.move_count += 1
        self.fitness += 10

        self.cell_x += self.vel[0]
        self.cell_y += self.vel[1]

        if self.cell_x == apple.cell_x and self.cell_y == apple.cell_y:
            apple.move(self)
            self.grow()
            self.move_count = 0
            self.fitness += 250

        for i in range(len(self.body)):
            self.body[i].update()
            if self.cell_x == self.body[i].cell_x and self.cell_y == self.body[i].cell_y:
                self.is_alive = False
                self.fitness -= 500
            if i == 0:
                self.body[i].vel = [self.cell_x - self.body[i].cell_x, self.cell_y - self.body[i].cell_y]
            else:
                self.body[i].vel = [self.body[i - 1].cell_x - self.body[i].cell_x,
                                    self.body[i - 1].cell_y - self.body[i].cell_y]

        if self.cell_x < 0 or self.cell_x >= self.grid_size or self.cell_y < 0 or self.cell_y >= self.grid_size:
            self.is_alive = False
            self.fitness -= 500

        if self.move_count > self.max_moves:
            self.is_alive = False
            self.fitness -= 100

        # --------------- Neural Network ---------------

        # Fitness Function
        if not self.is_alive:
            self.neural_net.fitness = 500 + self.fitness

        output = self.neural_net.get_output(self.get_nn_input(apple))

        if output == 0:
            self.move(0, -1)
        elif output == 1:
            self.move(0, 1)
        elif output == 2:
            self.move(-1, 0)
        elif output == 3:
            self.move(1, 0)

        return self.is_alive

    def get_nn_input(self, apple):
        # Find The distances in each direction to the closest body cell
        closest_body_up = closest_body_down = closest_body_left = closest_body_right = self.grid_size
        for i in range(len(self.body)):
            if self.cell_x == self.body[i].cell_x:
                if self.cell_y < self.body[i].cell_y:
                    if self.body[i].cell_y - self.cell_y < closest_body_down:
                        closest_body_down = self.body[i].cell_y - self.cell_y
                else:
                    if self.cell_y - self.body[i].cell_y < closest_body_up:
                        closest_body_up = self.cell_y - self.body[i].cell_y
            elif self.cell_y == self.body[i].cell_y:
                if self.cell_x > self.body[i].cell_x:
                    if self.cell_x - self.body[i].cell_x < closest_body_left:
                        closest_body_left = self.cell_x - self.body[i].cell_x
                else:
                    if self.body[i].cell_x - self.cell_x < closest_body_right:
                        closest_body_right = self.body[i].cell_x - self.cell_x

        # Find distances in each direction to the wall
        closest_wall_up = self.cell_y
        closest_wall_down = self.grid_size - self.cell_y
        closest_wall_left = self.cell_x
        closest_wall_right = self.grid_size - self.cell_x

        # Find differences in each axis to the apple
        if self.cell_y > apple.cell_y:
            apple_diff_up = self.cell_y - apple.cell_y
            apple_diff_down = self.grid_size - self.cell_y
        else:
            apple_diff_down = apple.cell_y - self.cell_y
            apple_diff_up = self.cell_y
        if self.cell_x > apple.cell_x:
            apple_diff_left = self.cell_x - apple.cell_x
            apple_diff_right = self.grid_size - self.cell_x
        else:
            apple_diff_right = apple.cell_x - self.cell_x
            apple_diff_left = self.cell_x


        # Normalize inputs
        inputs = [closest_wall_up, closest_wall_down, closest_wall_left, closest_wall_right,
                  apple_diff_up, apple_diff_down, apple_diff_left, apple_diff_right]

        for i in range(len(inputs)):
            inputs[i] = (inputs[i] - (self.grid_size / 2)) / (self.grid_size / 2)
            inputs[i] = 0 - inputs[i]

        return inputs

    def move(self, dx, dy):
        if len(self.body) == 0 or (self.cell_x + dx != self.body[0].cell_x and self.cell_y + dy != self.body[0].cell_y):
            self.vel = [dx, dy]

    def grow(self):
        if len(self.body) == 0:
            new_body = Body(self.cell_x - self.vel[0], self.cell_y - self.vel[1], self.size)
        else:
            new_body = Body(self.body[len(self.body) - 1].cell_x, self.body[len(self.body) - 1].cell_y, self.size)
        self.body.append(new_body)

    def draw(self, window):
        rect = Rectangle(Point((self.cell_x * self.size), (self.cell_y * self.size) + self.size),
                              Point((self.cell_x * self.size) + self.size, (self.cell_y * self.size)))
        rect.setFill('green')
        rect.setOutline('green')
        rect.draw(window)

        for i in range(len(self.body)):
            self.body[i].draw(window)
