import random


class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.stored_value = 0

    def randomize(self):
        self.bias = random.randint(-100, 100) / 100.0

    def get_output(self):
        return self.stored_value + self.bias
