from animal import Animal


class WarmBlooded(Animal):

    def __init__(self, cell):
        super().__init__(cell)
        self.temperature_sensibility = 0.1
        self.optimal_temperature = [5, 30]
        pass

    def eat(self):
        if self.cell.plant_nutrition > 0:
            if self.cell.plant_nutrition > self.kus:
                self.energy += self.kus
                self.cell.plant_nutrition -= self.kus
            else:
                self.energy += self.cell.plant_nutrition
                self.cell.plant_nutrition = 0
