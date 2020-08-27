import random
from graphics import *


class Connection:
    def __init__(self, neuron1, neuron2):
        self.weight = random.randint(-100, 100) / 100.0
        self.neuron1 = neuron1
        self.neuron2 = neuron2
        self.line = None

    def update_look(self):
        if self.weight >= 0:
            self.line.setFill('blue')
        else:
            self.line.setFill('red')

    def draw(self, size, window):
        self.line = Line(Point(self.neuron1.mid_point.x + size / 2, self.neuron1.mid_point.y),
                         Point(self.neuron2.mid_point.x - size / 2, self.neuron2.mid_point.y))
        self.line.draw(window)
