from graphics import *
from Game import Game
from pynput import keyboard


def main():
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


main()
