from random import randint

from cell import Cell
from coldblooded import ColdBlooded
from warmblooded import WarmBlooded
import numpy as np

FIELD_WIDTH = 150
FIELD_HEIGHT = 100
START_ANIMAL_NUMBER = 200
START_ANIMAL_RATIO = [50, 50]  # пропорция хладнокровных/теплокровных в %


def stage_generation():
    cells = [[Cell() for j in range(FIELD_HEIGHT)] for i in range(FIELD_WIDTH)]
    animals = []
    if START_ANIMAL_NUMBER <= FIELD_HEIGHT*FIELD_WIDTH:
        for i in range(START_ANIMAL_NUMBER):
            if sum(START_ANIMAL_RATIO) == 100:
                type_index = 'WARM' if randint(1, START_ANIMAL_RATIO[0]) else 'COLD'
                cell = None
                while not cell:
                    random_cell = cells[randint(0, FIELD_WIDTH - 1)][randint(0, FIELD_HEIGHT - 1)]
                    cell = random_cell if not random_cell.animal else None
                animals += [WarmBlooded(cell) if type_index == 'WARM' else ColdBlooded(cell)]
    return cells, animals
