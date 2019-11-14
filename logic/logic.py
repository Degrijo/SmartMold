from random import randint, random

import numpy as np

from logic.cell import Cell
from logic.cells_const import MAX_PLANTS_NUTRITION, FIELD_HEIGHT, FIELD_WIDTH, START_ANIMAL_NUMBER, START_ANIMAL_RATIO
from logic.coldblooded import ColdBlooded
from logic.warmblooded import WarmBlooded


def stage_generation():
    cells = [[Cell() for j in range(FIELD_HEIGHT)] for i in range(FIELD_WIDTH)]
    animals = []
    if START_ANIMAL_NUMBER <= FIELD_HEIGHT * FIELD_WIDTH:
        for i in range(START_ANIMAL_NUMBER):
            if sum(START_ANIMAL_RATIO) == 100:
                type_index = 'WARM' if randint(1, START_ANIMAL_RATIO[0]) else 'COLD'
                cell = None
                while not cell:
                    random_cell = cells[randint(0, FIELD_WIDTH - 1)][randint(0, FIELD_HEIGHT - 1)]
                    cell = random_cell if not random_cell.animal else None
                animals += [WarmBlooded(cell) if type_index == 'WARM' else ColdBlooded(cell)]
    init_cells_temperature(cells)

    return cells, animals

MIN_TEMPERATURE = -30
MAX_TEMPERATURE = 40

def init_cells_temperature(cells):
    width = len(cells)
    height = len(cells[1])
    k = (MAX_TEMPERATURE - MIN_TEMPERATURE) / ( height / 2)
    for row in range(width):
        for col in range(height):
            if row < height / 2:
                cells[row][col].temperature = MIN_TEMPERATURE + k * row #линейное распределение температуры
            else:
                cells[row][col].temperature = MAX_TEMPERATURE - k * row / 2 #линейное распределение температуры


def init_plants(cells):
    for row in range(cells.shape[0]):
        for col in range(cells.shape[1]):
            cells[row][col].plant_nutrition = random.uniform(0, MAX_PLANTS_NUTRITION)






