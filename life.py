"""
Implementation of Conway's Game of Life for the terminal in Python
"""

import random
import shutil
import time

WIDTH, HEIGHT = shutil.get_terminal_size()
STATES = ['░', '▓']
current_state = [random.choice(STATES) for _ in range(HEIGHT * WIDTH)]

def to_index(x, y):
    return ((y % HEIGHT) * WIDTH) + (x % WIDTH)

def von_neumann_neigbors(cell):
    # Von Neumann Neighborhood
    x, y = cell % WIDTH, cell // WIDTH
    yield to_index(x + 1, y)
    yield to_index(x - 1, y)
    yield to_index(x, y - 1)
    yield to_index(x, y + 1)


def moore_neighbors(cell):
    # Moore Neigborhood
    x, y = cell % WIDTH, cell // WIDTH
    yield from von_neumann_neigbors(cell)
    yield to_index(x + 1, y + 1)
    yield to_index(x + 1, y - 1)
    yield to_index(x - 1, y + 1)
    yield to_index(x - 1, y - 1)


def next_state(state):
    new_state = []
    for i, cell in enumerate(state):
        live_neighbors = sum(state[n_i] == '▓' for n_i in von_neumann_neigbors(i))

        if cell == '▓' and live_neighbors < 2:
            new_state.append('░')
        elif cell == '▓' and 2 <= live_neighbors <= 3:
            new_state.append('▓')
        elif cell == '▓' and live_neighbors > 3:
            new_state.append('░')
        elif cell == '░' and live_neighbors == 3:
            new_state.append('▓')
        else:
            new_state.append('░')
    return new_state

def print_state(state):
    for line in range(HEIGHT):
        print(''.join(state[line * WIDTH: (1 + line) * WIDTH]))

while True:
    print_state(current_state)
    current_state = next_state(current_state)
    time.sleep(1/10)
