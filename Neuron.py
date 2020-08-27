import random
import math
from graphics import *


class Neuron:
    def __init__(self, bias, b_activation, b_output, b_drawn):
        self.b_drawn = b_drawn
        self.bias = bias
        self.stored_value = 0
        if b_drawn:
            self.circle = None
            self.color = 'white'
        self.mid_point = None
        self.b_activation = b_activation
        self.b_output = b_output

    def randomize(self):
        self.bias = random.randint(-100, 100) / 100.0

    def get_output(self):
        # Get the output
        output = self.stored_value + self.bias
        if self.b_activation:
            output = 1 / (1 + math.exp(-output))

        # Edit the visuals if the Node has visuals
        if self.b_drawn and not self.b_output:
            old_color = self.color
            if output >= 0.5:
                self.color = 'blue'
            elif output >= 0:
                self.color = 'aqua'
            else:
                self.color = 'white'
            if self.color != old_color:
                self.circle.setFill(self.color)

        return output

    def look_fire(self):
        self.circle.setFill('blue')

    def look_dormant(self):
        self.circle.setFill('white')

    def draw(self, x, y, size, padding_x, padding_y, margin, window, layer_size, max_neurons):
        neuron_diff = max_neurons - layer_size
        neuron_diff_offset = (neuron_diff * (size + padding_y)) / 2
        self.mid_point = Point(((x + 1) * padding_x) + (x * size) + (size / 2),
                               ((y + 1) * padding_y) + (y * size) + (size / 2) + margin + neuron_diff_offset)
        self.circle = Circle(self.mid_point, size / 2)
        self.circle.setFill('white')
        self.circle.draw(window)
