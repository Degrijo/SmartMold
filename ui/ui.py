import random
import tkinter as tk
from time import sleep

import numpy as np
from colour import Color

MODE_ANIMALS = 'mode_animals'
MODE_ENERGY = 'mode_energy'
MODE_TEMPERATURE = 'mode_temperature'
MODE_PLANTS = 'mode_plants'
MODE_CORPSE = 'mode_corpse'

current_view_mode = MODE_ANIMALS
game_play = False

# время одного шага - 0.2сек
STEP_TIME = 200

# TODO добавить поле которое будет отображать текущее поколение и текущий ход
current_generation = 0
current_step = 0

###############################################################################
# параметры животных стартовые
MIN_ANIMAL_ENERGY = 20
MAX_ANIMAL_ENERGY = 100
COLD_BLOODED_OPTIMAL_TEMPERATURE = [10, 20]
COLD_BLOODED_TEMPERATURE_SENSIBILITY = 0.3
WARM_BLOODED_OPTIMAL_TEMPERATURE = [5, 30]
WARM_BLOODED_TEMPERATURE_SENSIBILITY = 0.1
###############################################################################


################################################################################
# параметры поля
FIELD_WIDTH = 150
FIELD_HEIGHT = 100
START_ANIMAL_NUMBER = 5000
START_ANIMAL_RATIO = [0.5, 0.5]  # пропорция хладнокровных/теплокровных в %
MIN_TEMPERATURE = -10
MAX_TEMPERATURE = 40
BASE_CELL_TEMPERATURE = 20
CORPSE_DECAY_TIME = 5
MAX_CORPSE_ENERGY = 50
MAX_PLANTS_NUTRITION = 40
#################################################################################

################################################################################
# методы для работы с цветом
warm_blooded_cell_color = "#8B1A1A"
cold_blooded_cell_color = "#104E8B"

empty_cell_color = "White"

min_energy_cell_color =   "#E0FFFF"
max_energy_cell_color = "#191970"

min_plants_cell_color = "#9AFF9A"
max_plants_cell_color = "#008000"

min_temperature_cell_color = "#F0E68C"
max_temperature_cell_color = "#FF4500"

min_corpse_cell_color = "#D3D3D3"
max_corpse_cell_color = "#363636"

gradient_color_count = 10


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def get_energy_color(energy):
    if energy == 0:
        return empty_cell_color
    min_color = Color(min_energy_cell_color)
    max_color = Color(max_energy_cell_color)
    col_n = round((MAX_ANIMAL_ENERGY - MIN_ANIMAL_ENERGY) / gradient_color_count)
    n = round((energy - MIN_ANIMAL_ENERGY) / col_n)
    return list(min_color.range_to(max_color, gradient_color_count))[n]


def get_animal_color(animal):
    if not animal:
        return empty_cell_color
    if type(animal) == WarmBlooded:
        return warm_blooded_cell_color
    else:
        return cold_blooded_cell_color


def get_plant_color(plant_nutrition):
    if plant_nutrition == 0:
        return empty_cell_color
    min_color = Color(min_plants_cell_color)
    max_color = Color(max_plants_cell_color)
    col_n = round((MAX_PLANTS_NUTRITION - 0) / gradient_color_count)
    n = round((plant_nutrition - 0) / col_n)
    return list(min_color.range_to(max_color, gradient_color_count))[n]


def get_corpse_color(corpse_energy):
    if corpse_energy == 0:
        return empty_cell_color
    min_color = Color(min_corpse_cell_color)
    max_color = Color(max_corpse_cell_color)
    col_n = round((MAX_CORPSE_ENERGY - 0) / gradient_color_count)
    n = round((corpse_energy -  0) / col_n)
    return list(min_color.range_to(max_color, gradient_color_count))[col_n]


def get_temperature_color(temperature):
    min_color = Color(min_temperature_cell_color)
    max_color = Color(max_temperature_cell_color)
    col_n = round((MAX_TEMPERATURE - MIN_TEMPERATURE) / gradient_color_count)
    n = round((temperature - MIN_TEMPERATURE) / col_n)
    result_color = list(min_color.range_to(max_color, gradient_color_count))[n]
    return  result_color

###################################################################################

###########################################################################################
# мутационные штучки
mutation_probability = 0.05
# вероятности различных мутаций
# 0 - простая мутация, 1 - инверсияб 2 - транслокация
different_mutation = {"simple": 0.5, "inversion": 0.3, "translocation": 0.2}
crossover_probability = 0.02

generation_steps = 5


def fitness(animal):
    return MAX_ANIMAL_ENERGY - animal.energy


def crossover(animal1, animal2, child):
    if random.random() < crossover_probability:
        # определяем точку разрыва и всё левую часть забираем от первого родителя, а правую от второго
        break_point = random.randint(0, len(animal1.actions_probability))
        child_genom = animal1.actions_probability[:break_point] + animal2.actions_probability[break_point:]
        child.actions_probabylity = child_genom
    return child


def mutation(animal):
    if random.random() < mutation_probability:
        keys = list(different_mutation.keys())
        values = list(different_mutation.values())
        key = np.random.choice(keys, p=values)
        if key == "simple":
            animal.actions_probability = simple_mutation(animal.actions_probability)
        elif key == "inversion":
            animal.actions_probability = inversion_mutation(animal.actions_probability)
        elif key == "translocation":
            animal.actions_probability = translocation_mutation(animal.actions_probability)
        else:
            pass


def simple_mutation(genom):
    gen_n = random.choice(range(len(genom)))
    genom[gen_n] += 1
    return genom


def inversion_mutation(genom):
    inversion_part_len = round(len(genom) / 3)
    inversion_part_start = random.randint(0, len(genom) - inversion_part_len)
    inversed_part = list(reversed(genom[inversion_part_start:inversion_part_start + inversion_part_len]))
    new_genom = genom[:inversion_part_start] + genom[inversion_part_start + inversion_part_len:]
    for i in range(len(inversed_part)):
        new_genom.insert(inversion_part_start + i, inversed_part[i])
    return new_genom


def translocation_mutation(genom):
    translocation_part_len = round(len(genom) / 3)
    translocation_part_start = random.randint(0, len(genom) - translocation_part_len)
    translocation_part_new_start = random.randint(0, len(genom) - translocation_part_len)

    translocation_part = genom[translocation_part_start:translocation_part_start + translocation_part_len]
    new_genom = genom[:translocation_part_start] + genom[translocation_part_start + translocation_part_len:]
    for i in range(translocation_part_len):
        new_genom.insert(translocation_part_new_start + i, translocation_part[i])
    return new_genom


########################################################################

################################################################################

cells = []
cold = []
warm = []
directions = {'LEFT-UP': 0, 'UP': 1, 'RIGHT-UP': 2,
              'LEFT': 3, 'RIGHT': 4,
              'LEFT-BOTTOM': 5, 'BOTTOM': 6, 'RIGHT-BOTTOM': 7}  # совспадает с номерами клеток соседей текущей
# actions 0-7 направления, 8 - питание, 9 - отдых и так два раза
actions = ["LEFT-UP", 'UP', 'RIGHT-UP', 'LEFT', 'RIGHT', 'LEFT-BOTTOM', 'BOTTOM', 'RIGHT-BOTTOM', 'NUTRITION', 'REST']


##################################################################################
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
        self.cell.animal = self
        self.actions_probability = [random.randint(1, 10) for i in range(len(actions))]

    def check_energy(self):
        if self.energy <= self.min_energy:  # смэрть
            self.cell.animal = None
            self.cell.add_corpse_energy(self.energy)
            self.energy = 0
        else:
            self.energy -= self.energy_debuff

    def move(self, direction):
        destination_cell = self.cell.nearest_cells[direction]
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
        return None

    def find_partner(self):
        return None

    def find_free_cell(self):
        for cell in self.cell.nearest_cells:
            if cell is not None and not cell.animal:
                return cell

    def step(self):
        s = sum(self.actions_probability)
        prob = []
        for i in range(len(self.actions_probability)):
            prob.append(self.actions_probability[i] / s)

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
        self.age += 1
        self.temperature_effect()
        self.check_energy()

    def temperature_effect(self):
        current_temperature = self.cell.temperature
        energy_debuff = abs(current_temperature - (
                self.optimal_temperature[1] - self.optimal_temperature[0]) / 2 * self.temperature_sensibility)
        # можно заменить линейную функцию на квадратичную или ещё какую-нибудь
        self.energy -= energy_debuff


class WarmBlooded(Animal):

    def __init__(self, cell):
        super().__init__(cell)
        self.energy = MAX_ANIMAL_ENERGY
        self.optimal_temperature = [0, 35]
        self.energy_debuff = 5
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

    def find_partner(self):
        cells = self.cell.nearest_cells
        for cell in cells:
            if cell:
                if isinstance(cell.animal, WarmBlooded):
                    return cell.animal

    def try_reproduce(self):
        if self.energy == 0:
            return
        partner = self.find_partner()
        if partner:
            child_cell = self.find_free_cell()
            if not child_cell:
                if partner.energy > self.energy:
                    child_cell = self.cell
                    self.cell = None
                    self.energy = 0
                else:
                    child_cell = partner.cell
                    partner.energy = 0
                    partner.cell = None
            child = WarmBlooded(child_cell)
            crossover(self, partner, child)
            mutation(child)
            child_cell.animal = child
            return child


class ColdBlooded(Animal):

    def __init__(self, cell):
        super().__init__(cell)
        self.energy = MAX_ANIMAL_ENERGY
        self.optimal_temperature = [15, 25]
        self.energy_debuff = 2
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
            if cell:
                if isinstance(cell.animal, ColdBlooded):
                    return cell.animal

    def try_reproduce(self):
        if self.energy == 0:
            return
        partner = self.find_partner()
        if partner:
            child_cell = self.find_free_cell()
            if not child_cell:
                if partner.energy > self.energy:
                    child_cell = self.cell
                    self.cell = None
                    self.energy = 0
                else:
                    child_cell = partner.cell
                    partner.energy = 0
                    partner.cell = None
            child = ColdBlooded(child_cell)
            crossover(self, partner, child)
            mutation(child)
            child_cell.animal = child
            return child


class Cell:
    def __init__(self):
        self.plant_nutrition = 0  # питательность растений на клетке
        self.temperature = BASE_CELL_TEMPERATURE
        self.corpse_energy = 0  # питательность трупов на клетке
        self.corpse_age = 0  # возраст трупов на клетке
        self.nearest_cells = [None] * 8  # +x, -x, +y, -y
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

    def color_by_view_mode(self, state):
        if state == MODE_ANIMALS:
            return get_animal_color(self.animal)
        elif state == MODE_ENERGY:
            energy = 0
            if self.animal:
                energy = self.animal.energy
            return get_energy_color(energy)
        elif state == MODE_PLANTS:
            return get_plant_color(self.plant_nutrition)
        elif state == MODE_TEMPERATURE:
            return get_temperature_color(self.temperature)
        elif state == MODE_CORPSE:
            return get_corpse_color(self.corpse_energy)


class FrontWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("960x540+300+150")
        self.root.minsize(700, 300)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.toolbar = tk.Frame(self.root, highlightthickness=1, highlightbackground='black', width=300, height=300)
        self.toolbar.grid(row=0, column=3, sticky='ns', padx=(10, 0), pady=0)
        self.view_button = [
            tk.Button(self.toolbar, text='Animals view', command=self.switch_mode_animals, bg='#8B1A1A',
                      activebackground='#e68c55',
                      activeforeground='white', width=40).grid(row=1, column=1, pady=(3, 10), sticky='we'),
            tk.Button(self.toolbar, text='Energy view', command=self.switch_mode_energy, bg='#E0FFFF',
                      activebackground='#e68c55',
                      activeforeground='white', width=40).grid(row=2, column=1, pady=(3, 10), sticky='we'),
            tk.Button(self.toolbar, text='Temperature view', command=self.switch_mode_temperature, bg='#F0E68C',
                      activebackground='#e68c55',
                      activeforeground='white', width=40).grid(row=3, column=1, pady=(3, 10), sticky='we'),
            tk.Button(self.toolbar, text='Corpse view', command=self.switch_mode_corpse, bg='#D3D3D3',
                      activebackground='#e68c55',
                      activeforeground='white', width=40).grid(row=4, column=1, pady=(3, 10), sticky='we')
        ]
        self.field = tk.Canvas(self.root, highlightthickness=1, highlightbackground='black',
                               bg='#f7d794', relief='ridge', scrollregion=(0, 0, 1190, 745))
        self.field.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nswe', padx=(0, 10), pady=(0, 10))
        self.buttonbar = tk.Frame(self.root, highlightbackground='black', width=200, height=70, highlightthickness=1)
        self.buttonbar.grid(row=3, column=0, columnspan=2, rowspan=1, sticky='we', padx=(0, 10), pady=(10, 0))
        self.buttonbar.grid_rowconfigure(0, weight=1)
        self.buttonbar.grid_columnconfigure(0, weight=30)
        self.buttonbar.grid_columnconfigure(1, weight=1)
        self.buttonbar.grid_columnconfigure(2, weight=1)
        self.buttons = [
            tk.Button(self.buttonbar, text='Play', command=self.play, bg='#8beb77', activebackground='#77eb8b',
                      activeforeground='white', width=10).grid(row=0, column=1, pady=(10, 3), sticky='we'),
            tk.Button(self.buttonbar, text='Pause', command=self.pause, bg='#e66e55', activebackground='#e68c55',
                      activeforeground='white', width=10).grid(row=1, column=1, pady=(3, 10), sticky='we')
        ]
        self.state = True
        self.run = False
        self.squares = []
        for x in range(FIELD_HEIGHT):  # vertical
            self.squares.append([])
            for y in range(FIELD_WIDTH):  # horizontal
                self.squares[x].append(self.field.create_rectangle(x * 1550 // FIELD_WIDTH, y * 950 // FIELD_HEIGHT,
                                        (x+1) * 1550 // FIELD_WIDTH, (y+1) * 950 // FIELD_HEIGHT))
        xbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        ybar = tk.Scrollbar(self.root)
        ybar.grid(row=0, column=2, rowspan=3, sticky='ns')
        xbar.grid(row=2, column=0, columnspan=2, sticky='we')
        self.field.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        xbar.config(command=self.field.xview)
        ybar.config(command=self.field.yview)
        self.root.attributes("-fullscreen", self.state)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.bind("<space>", self.change_run)
        stage_generation()
        self.refresh()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)

    def play(self):
        global game_play, current_generation, current_step
        game_play = True
        print("cold", len(cold))
        print("warm", len(warm))
        if game_play and len(cold) > 0 and len(warm):
            for i in range(generation_steps):
                do_step()
                current_step = i
                print("generation ", current_generation, "step ", current_step)
                self.refresh()
            do_reproduction()
            # sleep(1)
            print("cold", len(cold))
            print("warm", len(warm))
            current_generation += 1
            self.refresh()
        # self.run = True
        # game_play = True
        # self.buttons[0].config(state=tk.DISABLED)
        # self.buttons[1].config(state=tk.NORMAL)

    def pause(self):
        self.run = False
        game_play = False
        # self.buttons[1].config(state=tk.DISABLED)
        # self.buttons[0].config(state=tk.NORMAL)

    def change_run(self, event=None):
        self.run = not self.run
        # if self.run:
        #     self.buttons[0].config(state=tk.DISABLED)
        #     self.buttons[1].config(state=tk.NORMAL)
        # else:
        #     self.buttons[1].config(state=tk.DISABLED)
        #     self.buttons[0].config(state=tk.NORMAL)

    def refresh(self):
        for i in range(FIELD_HEIGHT):
            for j in range(FIELD_WIDTH):
                self.field.itemconfig(self.squares[i][j], fill=cells[i][j].color_by_view_mode(current_view_mode))

    def switch_mode_animals(self):
        global current_view_mode
        current_view_mode = MODE_ANIMALS
        self.refresh()

    def switch_mode_energy(self):
        global current_view_mode
        current_view_mode = MODE_ENERGY
        self.refresh()

    def switch_mode_temperature(self):
        global current_view_mode
        current_view_mode = MODE_TEMPERATURE
        self.refresh()

    def switch_mode_plants(self):
        global current_view_mode
        current_view_mode = MODE_PLANTS
        self.refresh()

    def switch_mode_corpse(self):
        global current_view_mode
        current_view_mode = MODE_CORPSE
        self.refresh()


def do_reproduction():
    global warm, cold
    warm_children = []
    for warm_a in warm:
        child = warm_a.try_reproduce()
        if child:
            warm_children.append(child)
    warm = list(filter(lambda animal: animal.energy != 0, warm))
    print("new warm ",len(warm_children))
    warm.extend(warm_children)

    cold_children = []
    for cold_a in cold:
        child = cold_a.try_reproduce()
        if child:
            cold_children.append(child)
    cold = list(filter(lambda animal: animal.energy != 0, cold))
    print("new cold ", len(cold_children))
    cold.extend(cold_children)


def stage_generation():
    global cells, warm, cold
    cells = [[Cell() for j in range(FIELD_WIDTH)] for i in range(FIELD_HEIGHT)]
    init_nearest_cells(cells)
    cold = []
    warm = []
    if START_ANIMAL_NUMBER <= FIELD_HEIGHT * FIELD_WIDTH:
        for i in range(START_ANIMAL_NUMBER):
            if sum(START_ANIMAL_RATIO) == 1:
                type_index = 'WARM' if random.random() < START_ANIMAL_RATIO[0] else 'COLD'
                cell = None
                while not cell:
                    random_cell = cells[random.randint(0, FIELD_HEIGHT - 1)][random.randint(0, FIELD_WIDTH - 1)]
                    cell = random_cell if not random_cell.animal else None
                if type_index == 'WARM':
                    warm.append(WarmBlooded(cell))
                else:
                    cold.append(ColdBlooded(cell))
    init_cells_temperature()
    init_plants()


def init_nearest_cells(cells):
    width = len(cells[0])
    height = len(cells)

    # заполняем соседей для некрайних клеток
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            cells[i][j].nearest_cells[0] = cells[i - 1][j - 1]
            cells[i][j].nearest_cells[1] = cells[i - 1][j]
            cells[i][j].nearest_cells[2] = cells[i - 1][j + 1]

            cells[i][j].nearest_cells[3] = cells[i][j - 1]
            cells[i][j].nearest_cells[4] = cells[i][j + 1]

            cells[i][j].nearest_cells[5] = cells[i + 1][j - 1]
            cells[i][j].nearest_cells[6] = cells[i + 1][j]
            cells[i][j].nearest_cells[7] = cells[i + 1][j + 1]

    # замыкаем левый и правый края и заполняем соседей для крайних клеток
    # левый край
    for i in range(height):
        cells[i][0].nearest_cells[3] = cells[i][width - 1]  # слева замыкается с правым краем
        if i != 0 and i != len(cells) - 1:
            cells[i][0].nearest_cells[0] = cells[i - 1][width - 1]
            cells[i][0].nearest_cells[5] = cells[i + 1][width - 1]

            cells[i][0].nearest_cells[1] = cells[i - 1][0]
            cells[i][0].nearest_cells[2] = cells[i - 1][1]
            cells[i][0].nearest_cells[4] = cells[i][1]
            cells[i][0].nearest_cells[6] = cells[i + 1][0]
            cells[i][0].nearest_cells[7] = cells[i + 1][1]
    # правый край
    for i in range(height):
        cells[i][width - 1].nearest_cells[4] = cells[i][0]  # справа замыкаетя с левым краем
        if i != 0 and i != height - 1:
            cells[i][width - 1].nearest_cells[2] = cells[i - 1][0]
            cells[i][width - 1].nearest_cells[7] = cells[i + 1][0]

            cells[i][width - 1].nearest_cells[0] = cells[i - 1][0]
            cells[i][width - 1].nearest_cells[1] = cells[i - 1][width - 1]
            cells[i][width - 1].nearest_cells[3] = cells[i][width - 2]
            cells[i][width - 1].nearest_cells[5] = cells[i + 1][width - 2]
            cells[i][width - 1].nearest_cells[6] = cells[i + 1][width - 1]

    #верхний и нижний края
    for i in range(1, width-1):
        #верхний
        cells[0][i].nearest_cells[3] = cells[0][i - 1]
        cells[0][i].nearest_cells[4] = cells[0][i + 1]
        cells[0][i].nearest_cells[5] = cells[1][i - 1]
        cells[0][i].nearest_cells[6] = cells[1][i]
        cells[0][i].nearest_cells[7] = cells[1][i + 1]
        #нижний
        cells[height - 1 ][i].nearest_cells[0] = cells[height - 2][i - 1]
        cells[height - 1 ][i].nearest_cells[1] = cells[height - 2][i]
        cells[height - 1 ][i].nearest_cells[2] = cells[height - 2][i + 1]
        cells[height - 1 ][i].nearest_cells[3] = cells[height - 1][i - 1]
        cells[height - 1 ][i].nearest_cells[4] = cells[height - 1][i + 1]

    # угловые
    # левый верхний
    cells[0][0].nearest_cells[4] = cells[0][1]
    cells[0][0].nearest_cells[6] = cells[1][0]
    cells[0][0].nearest_cells[7] = cells[1][1]
    # правый нижний
    cells[height - 1][width - 1].nearest_cells[0] = cells[height - 2][width - 2]
    cells[height - 1][width - 1].nearest_cells[1] = cells[height - 2][width - 1]
    cells[height - 1][width - 1].nearest_cells[3] = cells[height - 1][width - 2]
    # правыц верхний
    cells[0][width - 1].nearest_cells[3] = cells[0][width - 2]
    cells[0][width - 1].nearest_cells[5] = cells[1][width - 2]
    cells[0][width - 1].nearest_cells[6] = cells[1][width - 2]
    # левый нижний
    cells[height - 1][0].nearest_cells[1] = cells[height - 2][0]
    cells[height - 1][0].nearest_cells[2] = cells[height - 2][1]
    cells[height - 1][0].nearest_cells[4] = cells[height - 1][1]


def init_cells_temperature():
    width = len(cells[1])
    height = len(cells)
    k = (MAX_TEMPERATURE - MIN_TEMPERATURE) / (height / 2)
    for row in range(height):
        for col in range(width):
            if row < (height / 2):
                cells[row][col].temperature = MIN_TEMPERATURE + k * row  # линейное распределение температуры
            else:
                cells[row][col].temperature = MAX_TEMPERATURE - k * row // 2  # линейное распределение температуры


def init_plants():
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            cells[row][col].plant_nutrition = random.uniform(0, MAX_PLANTS_NUTRITION)


def do_step():
    global warm, cold
    for warm_animal in warm:
        warm_animal.step()
    warm = list(filter(lambda animal: animal.energy != 0, warm))
    for cold_animal in cold:
        cold_animal.step()
    cold = list(filter(lambda animal: animal.energy != 0, cold))


def start_game(window):
    global game_play, current_generation, current_step
    game_play = True
    print("cold", len(cold))
    print("warm", len(warm))
    while game_play and len(cold) > 0 and len(warm):
        for i in range(generation_steps):
            do_step()
            current_step = i
            print("generation " ,current_generation ,"step ", current_step)
            window.refresh()
        do_reproduction()
        sleep(1)
        print("cold" , len(cold))
        print("warm" , len(warm))
        current_generation += 1
        window.refresh()


if __name__ == '__main__':
    root = tk.Tk()
    fw = FrontWindow(root)
    root.mainloop()
