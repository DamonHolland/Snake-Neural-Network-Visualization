import random
from graphics import *


class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.stored_value = 0
        self.circle = None
        self.mid_point = None

    def randomize(self):
        self.bias = random.randint(-100, 100) / 100.0

    def get_output(self):
        return self.stored_value + self.bias

    def draw(self, x, y, size, padding_x, padding_y, margin, window, layer_size, max_neurons):
        neuron_diff = max_neurons - layer_size
        neuron_diff_offset = (neuron_diff * (size + padding_y)) / 2
        self.mid_point = Point(((x + 1) * padding_x) + (x * size) + (size / 2),
                               ((y + 1) * padding_y) + (y * size) + (size / 2) + margin + neuron_diff_offset)
        self.circle = Circle(self.mid_point, size / 2)
        self.circle.setFill('white')
        self.circle.draw(window)
