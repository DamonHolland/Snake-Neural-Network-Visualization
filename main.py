from graphics import *
from Game import Game
from pynput import keyboard
from NeuralNetwork import NeuralNetwork


def main():
    # Neural Network Configuration
    num_inputs = 6
    num_hidden_layers = 2
    num_outputs = 4
    neurons_in_hidden_layers = [5, 5]

    # Neural Network Visuals Configuration
    neuron_size = 64
    neuron_padding_x = 160
    neuron_padding_y = 64
    top_padding = 128

    window_nn = GraphWin("Neural Network",
                         ((2 + num_hidden_layers) * (neuron_size + neuron_padding_x) + neuron_padding_x),
                         ((num_inputs * (neuron_size + neuron_padding_y)) + neuron_padding_y) + top_padding)
    window_nn.setBackground('black')

    net = NeuralNetwork(num_inputs, num_hidden_layers, num_outputs, neurons_in_hidden_layers)

    inputs = [2, 2, 2, 2, 2, 2]

    net.get_output(inputs)

    net.draw_neurons(neuron_size, neuron_padding_x, neuron_padding_y, top_padding, window_nn)
    net.draw_connections(neuron_size, window_nn)
    net.update_look()

    fps = 10
    grid_size = 24
    cell_size = 32

    window = GraphWin("Snake", grid_size * cell_size, grid_size * cell_size)
    window.setBackground('black')

    while window.isOpen():
        is_running = True
        game = Game(grid_size, cell_size, window)
        listener = keyboard.Listener(on_press=game.on_press, on_release=0)
        listener.start()

        while is_running:
            last_frame_time = time.time()

            is_running = game.update()

            current_time = time.time()
            sleep_time = 1.0 / fps - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

        for item in window.items[:]:
            item.undraw()

    return 0


main()
