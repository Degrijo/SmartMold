from logic.cells_const import BASE_CELL_TEMPERATURE, CORPSE_DECAY_TIME
from ui.color_utils import empty_cell_color, get_energy_color, get_animal_color, get_plant_color, get_corpse_color
from logic.mods import MODE_ANIMALS, MODE_ENERGY, MODE_PLANTS, MODE_CORPSE


class Cell:
    def __init__(self):
        self.plant_nutrition = 0  # питательность растений на клетке
        self.temperature = BASE_CELL_TEMPERATURE
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
        if self.corpse_energy > 0 and self.corpse_age < CORPSE_DECAY_TIME:
            self.corpse_age += 1
        elif self.corpse_age == CORPSE_DECAY_TIME:
            self.corpse_age = 0
            self.plant_nutrition += self.corpse_energy
            self.corpse_energy = 0
        elif self.corpse_energy == 0:
            self.corpse_age = 0

    @property
    def color(self):
        if self.plant_nutrition and self.animal:
            return 'White'
        elif self.plant_nutrition:
            return "White"
        elif self.animal:
            return 'White'


def color_by_view_mode(self, state):
    col = empty_cell_color
    if state == MODE_ANIMALS:
        return get_animal_color(self.animal)
    elif state == MODE_ENERGY:
        energy = self.animal.energy | 0
        return get_energy_color(energy)
    elif state == MODE_PLANTS:
        return get_plant_color(self.plant_nutrition)
    elif state == MODE_CORPSE:
        return get_corpse_color(self.corpse_energy)
