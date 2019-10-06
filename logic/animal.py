import numpy as np


directions = {'LEFT-UP': 0, 'UP': 1, 'RIGHT-UP': 2,
              'LEFT': 3, 'RIGHT': 4,
              'LEFT-BOTTOM': 5, 'BOTTOM': 6, 'RIGHT-BOTTOM': 7}  # совспадает с номерами клеток соседей текущей


class Animal:

    def __init__(self, cell):
        self.max_energy = 100
        self.min_energy = 20  # Энергия ниже которой животное помирает и становится трупом на клетке
        self.energy = 0
        self.energy_debuff = 0
        self.passive_energy_reduction = 0

        self.optimal_temperature = 0
        self.temperature_sensibility = 0

        self.kus = 0
        self.cell = cell

        dirs = {dir: 0.1 for dir in directions.keys()}
        other = {'REPRODUCTION': 0.1,
                 'NUTRITION': 0.1,
                 'REST': 0.1}
        self.actions_probability = dict(list(dirs.items()) + list(other.items()))

    def move(self, direction):
        cell_n = direction[direction]
        destination_cell = self.cell.nearest_cells[cell_n]
        if destination_cell is None:
            return -1
        if destination_cell.animal is None:
            self.cell.animal = None
            self.cell = destination_cell
            destination_cell.animal = self

    def eat(self):
        pass

    def rest(self):
        pass

    def step(self):
        action = np.random.choice(self.actions_probability.keys(),
                                  p=self.actions_probability.values())  # порядок не потеряется?
        if (action in directions):
            self.move(directions[action])
        elif action == 'REPRODUCTION':
            pass
        elif action == 'NUTRITION':
            pass
        elif action == 'REST':
            pass

        self.temperature_effect()
        self.checkEnergy()

    def check_energy(self):
        if self.energy <= self.min_energy:  # смэрть
            self.cell.animal = None
            self.cell.add_corpse_energy(self.energy)
        else:
            self.energy -= self.energy_debuff

    def temperature_effect(self):
        current_temperature = self.cell.temperature
        energy_debuff = abs(current_temperature - (
                self.optimal_temperature[1] - self.optimal_temperature[0]) / 2 * self.temperature_sensibility)
        # можно заменить линейную функцию на квадратичную или ещё какую-нибудь
        self.energy -= energy_debuff
