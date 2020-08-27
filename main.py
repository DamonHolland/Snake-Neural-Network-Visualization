from graphics import *
from Controller import Controller


def main():
    # Neural Network Configuration
    num_inputs = 6
    num_hidden_layers = 2
    num_outputs = 4
    neurons_in_hidden_layers = [5, 5]
    num_snakes = 100

    # Neural Network Visuals Configuration
    neuron_size = 64
    neuron_padding_x = 160
    neuron_padding_y = 64
    top_padding = 128

    # Performance Configuration
    fps = 10
    performance_sum = 0
    performance_check = 30
    performance_counter = 0
    grid_size = 24
    cell_size = 32

    window_nn = GraphWin("Neural Network",
                         ((2 + num_hidden_layers) * (neuron_size + neuron_padding_x) + neuron_padding_x),
                         ((num_inputs * (neuron_size + neuron_padding_y)) + neuron_padding_y) + top_padding,
                         autoflush=False)
    window_nn.setBackground('black')

    window = GraphWin("Snake", grid_size * cell_size, grid_size * cell_size)
    window.setBackground('black')

    while window.isOpen() and window_nn.isOpen():
        controller = Controller(num_snakes, grid_size, cell_size, window, num_inputs, num_hidden_layers, num_outputs,
                                neurons_in_hidden_layers, neuron_size, neuron_padding_x, neuron_padding_y,
                                top_padding, window_nn)

        while controller.simulation_running:
            last_frame_time = time.time()

            # Game Loop
            controller.update()

            # Performance Checks
            current_time = time.time()
            sleep_time = 1.0 / fps - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            performance_counter += 1
            performance_sum += ((1.0 / fps) - sleep_time) / (1.0 / fps)
            if performance_counter == performance_check:
                print("Performance: " + str(performance_sum / performance_check))
                performance_counter = 0
                performance_sum = 0

    return 0


main()
