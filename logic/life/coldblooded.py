from logic.life.animal import Animal


class ColdBlooded(Animal):
    def __init__(self, cell):
        super.__init__(cell)
        self.temperature_sensibility = 0.5
        self.optimal_temperature = [15, 20]

    def eat(self):
        if self.cell.corpse_energy > 0:
            if self.cell.corpse_energy > self.kus:
                self.energy += self.kus
                self.cell.corpse_energy -= self.kus
            else:
                self.energy += self.cell.corpse_energy
                self.cell.corpse_energy = 0
