from graphics import *
from Controller import Controller


def main():
    # Neural Network Configuration
    num_inputs = 8
    neurons_in_hidden_layers = [8]
    num_outputs = 4
    num_snakes = 500

    most_neurons = num_inputs
    if num_outputs > most_neurons:
        most_neurons = num_outputs
    for i in range(len(neurons_in_hidden_layers)):
        if neurons_in_hidden_layers[i] > most_neurons:
            most_neurons = neurons_in_hidden_layers[i]

    # Genetic Algorithm Configuration
    num_best_snakes = 50
    num_crossovers = 250
    mutation_rate = 50

    # Neural Network Visuals Configuration
    neuron_size = 48
    neuron_padding_x = 96
    neuron_padding_y = 48
    top_padding = 64

    # Performance Configuration
    target_fps = 30
    performance_sum = 0
    performance_check = 30
    performance_counter = 0

    # Grid configuration
    grid_size = 15
    cell_size = 32

    window_nn = GraphWin("Neural Network",
                         ((2 + len(neurons_in_hidden_layers)) * (neuron_size + neuron_padding_x) + neuron_padding_x),
                         ((most_neurons * (neuron_size + neuron_padding_y)) + neuron_padding_y) + top_padding,
                         autoflush=False)
    window_nn.setBackground('black')

    window = GraphWin("Snake", grid_size * cell_size, grid_size * cell_size, autoflush=False)
    window.setBackground('black')

    while window.isOpen() and window_nn.isOpen():
        controller = Controller(num_snakes, grid_size, cell_size, window, num_inputs, len(neurons_in_hidden_layers),
                                num_outputs, neurons_in_hidden_layers, neuron_size, neuron_padding_x, neuron_padding_y,
                                top_padding, most_neurons, window_nn, num_best_snakes, num_crossovers, mutation_rate)

        while controller.simulation_running:
            last_frame_time = time.time()

            # Game Loop
            controller.update()

            # Performance Checks
            current_time = time.time()
            sleep_time = 1.0 / target_fps - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            performance_counter += 1
            current_time = time.time()
            performance_sum += 1.0 / (current_time - last_frame_time)
            if performance_counter == performance_check:
                print("Average FPS: " + str(performance_sum / performance_check) + " | Target FPS: " + str(target_fps))
                performance_counter = 0
                performance_sum = 0

    return 0


main()
