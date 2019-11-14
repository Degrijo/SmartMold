from logic.animal import Animal
from logic.animals_const import WARM_BLOODED_TEMPERATURE_SENSIBILITY, WARM_BLOODED_OPTIMAL_TEMPERATURE


class WarmBlooded(Animal):

    def __init__(self, cell):
        super().__init__(cell)
        self.temperature_sensibility = WARM_BLOODED_TEMPERATURE_SENSIBILITY
        self.optimal_temperature = WARM_BLOODED_OPTIMAL_TEMPERATURE

    def eat(self):
        if self.cell.plant_nutrition > 0:
            if self.cell.plant_nutrition > self.kus:
                self.energy += self.kus
                self.cell.plant_nutrition -= self.kus
            else:
                self.energy += self.cell.plant_nutrition
                self.cell.plant_nutrition = 0


