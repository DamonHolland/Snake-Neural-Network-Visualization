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
        self.total_moves = 0

    def update(self, apple):
        self.move_count += 1
        self.total_moves += 1

        self.cell_x += self.vel[0]
        self.cell_y += self.vel[1]

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

        if self.cell_x < 0 or self.cell_x >= self.grid_size or self.cell_y < 0 or self.cell_y >= self.grid_size:
            self.is_alive = False

        if self.move_count > self.max_moves:
            self.is_alive = False

        # --------------- Neural Network ---------------

        # Fitness Function
        if not self.is_alive:
            self.neural_net.fitness = int (self.total_moves + ((len(self.body) * len(self.body)) * 5) -
                                           (0.35 * (self.total_moves ** 1.2)))

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
        # Find if there is a body cell in each direction
        is_cell_up = is_cell_down = is_cell_left = is_cell_right = 0
        for i in range(len(self.body)):
            if self.cell_x == self.body[i].cell_x:
                if self.cell_y - 1 == self.body[i].cell_y:
                    is_cell_up = 1
                elif self.cell_y + 1 == self.body[i].cell_y:
                    is_cell_down = 1
            elif self.cell_y == self.body[i].cell_y:
                if self.cell_x - 1 == self.body[i].cell_x:
                    is_cell_left = 1
                elif self.cell_x + 1 == self.body[i].cell_x:
                    is_cell_right = 1
        # Find if there is a wall in each direction
        if self.cell_y - 1 < 0:
            is_cell_up = 1
        if self.cell_y + 1 >= self.grid_size:
            is_cell_down = 1
        if self.cell_x - 1 < 0:
            is_cell_left = 1
        if self.cell_x + 1 >= self.grid_size:
            is_cell_right = 1

        # Find differences in each axis to the apple
        is_apple_up = is_apple_down = is_apple_left = is_apple_right = 0
        if self.cell_y > apple.cell_y:
            is_apple_up = 1
        elif self.cell_y < apple.cell_y:
            is_apple_down = 1
        if self.cell_x > apple.cell_x:
            is_apple_left = 1
        elif self.cell_x < apple.cell_x:
            is_apple_right = 1

        #Normalize inputs
        is_cell_up = is_cell_up * 2 - 1
        is_cell_down = is_cell_down * 2 - 1
        is_cell_left = is_cell_left * 2 - 1
        is_cell_right = is_cell_right * 2 - 1
        is_apple_up = is_apple_up * 2 - 1
        is_apple_down = is_apple_down * 2 - 1
        is_apple_left = is_apple_left * 2 - 1
        is_apple_right = is_apple_right * 2 - 1


        #Fill input array with previously calculated values
        inputs = [is_cell_up, is_cell_down, is_cell_left, is_cell_right,
                  is_apple_up, is_apple_down, is_apple_left, is_apple_right]

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
