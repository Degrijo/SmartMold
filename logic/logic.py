import random
import numpy as np

from logic.animal import Animal
from logic.animals_const import MAX_ANIMAL_ENERGY

mutation_probability = 0.05
# вероятности различных мутаций
# 0 - простая мутация, 1 - инверсияб 2 - транслокация
different_mutation = {"simple": 0.5, "inversion": 0.3, "translocation": 0.2}
crossover_probability = 0.02

generation_steps = 10


def fitness(animal):
    return MAX_ANIMAL_ENERGY - animal.energy


def crossover(animal1, animal2, child):
    if random.random() < crossover_probability:
        #определяем точку разрыва и всё левую часть забираем от первого родителя, а правую от второго
        break_point = random.randint(0, len(animal1.action_probability))
        child_genom = animal1.action_probability[:break_point] + animal2.action_probability[break_point:]
        child.action_probabylity = child_genom
    return child

def mutation(animal):
    if random.random() < mutation_probability:
        key = np.random.choice(different_mutation.keys(), p=different_mutation.values())
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
    for i in range(len(genom)):
        new_genom.insert(inversion_part_start + i, inversed_part[i])
    return new_genom


def translocation_mutation(genom):
    translocation_part_len = round(len(genom) / 3)
    translocation_part_start = random.randint(0, len(genom) - translocation_part_len)
    translocation_part_new_start = random.randint(0, len(genom) - translocation_part_len)

    translocation_part = genom[translocation_part_start:translocation_part_len]
    new_genom = genom[:translocation_part_start] + genom[translocation_part_start + translocation_part_len:]
    for i in range(translocation_part_len):
        new_genom.insert(translocation_part_new_start + i, translocation_part[i])
    return new_genom
