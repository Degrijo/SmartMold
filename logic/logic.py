import random

from cell import Cell
from coldblooded import ColdBlooded
from warmblooded import WarmBlooded
from ui.ui import FIELD_WIDTH, FIELD_HEIGHT
import numpy as np


START_ANIMAL_NUMBER = 200
START_ANIMAL_RATIO = [1, 1]  # пропорция хладнокровных/теплокровных


def start_game():
    cells = []
    for i in range(FIELD_HEIGHT):
        cells.append([])
        for j in range(FIELD_WIDTH):
            cells[i].append(Cell())

    animals = []
    for i in range(START_ANIMAL_NUMBER):
        type_index = np.random.choice(['WARM', 'COLD'], p=START_ANIMAL_RATIO)
        cell = None
        while cell is None:
            random_cell = cells[random.randint(0, FIELD_HEIGHT)][0, FIELD_WIDTH]
            if random_cell.animal is None:
                cell = random_cell
        if type_index == 'WARM':
            animal = WarmBlooded(cell)
            animals.append(animal)
        else:
            animal = ColdBlooded(cell)
            animals.append(animal)


start_game()
