import random


class Connection:
    def __init__(self, neuron1, neuron2):
        self.weight = random.randint(-100, 100) / 100.0
        self.neuron1 = neuron1
        self.neuron2 = neuron2
