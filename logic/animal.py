import random

import numpy as np

from logic.animals_const import MAX_ANIMAL_ENERGY, MIN_ANIMAL_ENERGY
from logic.logic import crossover, mutation

directions = {'LEFT-UP': 0, 'UP': 1, 'RIGHT-UP': 2,
              'LEFT': 3, 'RIGHT': 4,
              'LEFT-BOTTOM': 5, 'BOTTOM': 6, 'RIGHT-BOTTOM': 7}  # совспадает с номерами клеток соседей текущей
# actions 0-7 направления, 8 - питание, 9 - отдых и так два раза
actions = ["LEFT-UP", 'UP', 'RIGHT-UP', 'LEFT', 'RIGHT', 'LEFT-BOTTOM', 'BOTTOM', 'RIGHT-BOTTOM', 'NUTRITION', 'REST']


class Animal:

    def __init__(self, cell):
        self.max_energy = MAX_ANIMAL_ENERGY
        self.min_energy = MIN_ANIMAL_ENERGY  # Энергия ниже которой животное помирает и становится трупом на клетке
        self.energy = 0
        self.energy_debuff = 0
        self.passive_energy_reduction = 0
        self.optimal_temperature = 0
        self.temperature_sensibility = 0
        self.kus = 0
        self.age = 0
        self.cell = cell
        self.actions_probability = [random.randint(1, 10) for i in range(len(actions))]

    def check_energy(self):
        if self.energy <= self.min_energy:  # смэрть
            self.cell.animal = None
            self.cell.add_corpse_energy(self.energy)
            self.energy = 0
        else:
            self.energy -= self.energy_debuff

    def move(self, direction):
        cell_n = direction[direction]
        destination_cell = self.cell.nearest_cells[cell_n]
        if not destination_cell:
            return -1
        if not destination_cell.animal:
            self.cell.animal = None
            self.cell = destination_cell
            destination_cell.animal = self

    def eat(self):
        pass

    def rest(self):
        pass

    def try_reproduce(self):
        partner = self.find_partner()
        if partner:
            child_cell = self.find_free_cell()
            if not child_cell:
                if partner.energy > self.energy:
                    child_cell = self.cell
                    self.cell = None
                    self.energy = 0
                else :
                    child_cell = partner.cell
                    partner.energy = 0
                    partner.cell = None
            child = Animal(child_cell)
            crossover(self, partner, child)
            mutation(child)
            child_cell.animal = child

    def find_partner(self):
        return None

    def find_free_cell(self):
        cells = self.cell.nearest_cells
        for cell in cells:
            if not cell.animal:
                return cell

    def step(self):
        sum = sum(self.actions_probability)
        prob = []
        for i in range(len(self.actions_probability)):
            prob[i] = self.actions_probability[i] / sum

        # для удобства работы с мутациями и проч.
        # вероятности вычисляются для каждого действия в отдельности, как части общей суммы значений действий
        action_n = np.random.choice(range(len(self.actions_probability)),
                                    p=prob)
        action = actions[action_n]

        if (action in directions):
            self.move(directions[action])
        elif action == 'NUTRITION':
            pass
        elif action == 'REST':
            pass
        self.age +=1
        self.temperature_effect()
        self.check_energy()

    def temperature_effect(self):
        current_temperature = self.cell.temperature
        energy_debuff = abs(current_temperature - (
                self.optimal_temperature[1] - self.optimal_temperature[0]) / 2 * self.temperature_sensibility)
        # можно заменить линейную функцию на квадратичную или ещё какую-нибудь
        self.energy -= energy_debuff
