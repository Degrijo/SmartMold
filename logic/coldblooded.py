from logic.animal import Animal
from logic.animals_const import COLD_BLOODED_OPTIMAL_TEMPERATURE, COLD_BLOODED_TEMPERATURE_SENSIBILITY


class ColdBlooded(Animal):

    def __init__(self, cell):
        super().__init__(cell)
        self.optimal_temperature = [15, 25]
        self.temperature_sensibility = COLD_BLOODED_TEMPERATURE_SENSIBILITY
        self.optimal_temperature = COLD_BLOODED_OPTIMAL_TEMPERATURE

    def eat(self):
        if self.cell.corpse_energy > 0:
            if self.cell.corpse_energy > self.kus:
                self.energy += self.kus
                self.cell.corpse_energy -= self.kus
            else:
                self.energy += self.cell.corpse_energy
                self.cell.corpse_energy = 0

    def find_partner(self):
        cells = self.cell.nearest_cells
        for cell in cells:
            if isinstance(cell.animal, ColdBlooded):
                return cell.animal