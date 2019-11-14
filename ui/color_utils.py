from colour import Color

from logic.animals_const import MIN_ANIMAL_ENERGY, MAX_ANIMAL_ENERGY
from logic.cells_const import MAX_PLANTS_NUTRITION, MAX_CORPSE_ENERGY
from logic.warmblooded import WarmBlooded

warm_blooded_cell_color =(139, 26, 26) #8B1A1A
cold_blooded_cell_color = (16, 78, 139) #104E8B

empty_cell_color ="White"

min_energy_cell_color = (224,255,255) #E0FFFF
max_energy_cell_color = (25,25,112)	 #191970

min_plants_cell_color =(154, 255, 154) #9AFF9A
max_plants_cell_color = (0,128,0)#008000

min_temperature_cell_color =(240,230,140) #F0E68C
max_temperature_cell_color = (255,69,0)	#FF4500

min_corpse_cell_color =(211, 211, 211) #D3D3D3
max_corpse_cell_color = (54, 54, 54) #363636

gradient_color_count = 10


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def get_energy_color(energy):
    if energy == 0:
        return empty_cell_color
    min_color = Color(min_energy_cell_color)
    max_color = Color(max_energy_cell_color)
    col_n = round((MAX_ANIMAL_ENERGY - MIN_ANIMAL_ENERGY)/gradient_color_count)
    return list(min_color.range_to(max_color, gradient_color_count))[col_n]

def get_animal_color(animal):
    if type(animal) == WarmBlooded:
        return rgb_to_hex(warm_blooded_cell_color)
    else:
        return rgb_to_hex(cold_blooded_cell_color)

def get_plant_color(plant_nutrition):
    if plant_nutrition == 0:
        return empty_cell_color
    min_color = Color(min_plants_cell_color)
    max_color = Color(max_plants_cell_color)
    col_n = round((MAX_PLANTS_NUTRITION - 0)/gradient_color_count)
    return list(min_color.range_to(max_color, gradient_color_count))[col_n]


def get_corpse_color(corpse_energy):
    if corpse_energy == 0:
        return empty_cell_color
    min_color = Color(min_corpse_cell_color)
    max_color = Color(max_corpse_cell_color)
    col_n = round((MAX_CORPSE_ENERGY - 0)/gradient_color_count)
    return list(min_color.range_to(max_color, gradient_color_count))[col_n]
