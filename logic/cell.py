class Cell:
    corpse_decay_time = 5  # время разложения трупа

    def __init__(self):
        self.plant_nutrition = 0  # питательность растений на клетке
        self.temperature = 20
        self.corpse_energy = 0  # питательность трупов на клетке
        self.corpse_age = 0  # возраст трупов на клетке
        self.nearest_cells = []  # +x, -x, +y, -y
        """
        Ближайшие клетки
        012
        3 4
        567 - расположение
        """
        self.animal = None

    def step(self):
        self.check_corpses()

    def add_corpse_energy(self, energy):
        self.corpse_energy += energy
        self.corpse_age = 0

    def check_corpses(self):
        if self.corpse_energy > 0 and self.corpse_age < self.corpse_decay_time:
            self.corpse_age += 1
        elif self.corpse_age == self.corpse_decay_time:
            self.corpse_age = 0
            self.plant_nutrition += self.corpse_energy
            self.corpse_energy = 0
        elif self.corpse_energy == 0:
            self.corpse_age = 0

    @property
    def color(self):
        if self.plant_nutrition and self.animal:
            return '#a44b16'
        elif self.plant_nutrition:
            return '#77eb8b'
        elif self.animal:
            return '#e6556e'
