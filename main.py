import random
import math
import numpy as np
import matplotlib.pyplot as plt

from random import randint
from copy import copy

data = np.loadtxt('cidades.mat')

x = data[0]
y = data[1]

chromosome_fitness = {}
to_plot = []
total_population = 0


def get_initial_possibilities():
    matriz = [[None] * 20 for _ in range(20)]
    for idx_l, line in enumerate(matriz):
        used_numbers = set()
        for idx_c, _ in enumerate(line):
            random_number = randint(1, 20)
            while random_number in used_numbers:
                random_number = randint(1, 20)

            matriz[idx_l][idx_c] = random_number
            used_numbers.add(random_number)

    return matriz


def get_euclidian_distance(gen_a, gen_b):
    dis_a_x = x[gen_a - 1]
    dis_a_y = y[gen_a - 1]
    dis_b_x = x[gen_b - 1]
    dis_b_y = y[gen_b - 1]
    dis = np.sqrt(math.pow((dis_a_x - dis_b_x), 2) + math.pow((dis_a_y - dis_b_y), 2))
    return dis


def get_fitness(distances):
    return sum(distances)


def roulette(matriz_c):
    probabilities = []
    for idx, _ in enumerate(matriz_c):
        for i in range(10 - idx):
            probabilities.append(idx)

    pairs_fathers_1 = []
    pairs_fathers_2 = []
    for _ in range(5):
        father1, father2 = matriz_c[random.choice(probabilities)], matriz_c[random.choice(probabilities)]
        pairs_fathers_1.append(father1)
        pairs_fathers_2.append(father2)

    return pairs_fathers_1, pairs_fathers_2


def order_by_fitness(matriz_c, chromosome_fitness):
    matriz_sorted = sorted(chromosome_fitness.items(), key=lambda item: item[1])
    matriz_updated = [[None] * 20 for _ in range(20)]
    for idx_row, chromosome in enumerate(matriz_sorted):
        matriz_updated[idx_row] = matriz_c[chromosome[0]]

    matriz_c = matriz_updated
    return matriz_c[:10]


def duplicate_gene(father, random):
    if len(father) != len(set(father)):
        pos_duplicated = [i for i, x in enumerate(father) if father.count(x) > 1]

        if pos_duplicated[0] == random:
            return pos_duplicated[1]
        return pos_duplicated[0]

    return None


def crossing_over(father1, father2):
    random_number = random.randint(0, 19)
    son1 = copy(father1)
    son2 = copy(father2)
    temp = son1[random_number]
    son1[random_number] = son2[random_number]
    son2[random_number] = temp
    duplicated_gen_pos = random_number
    if son1 != son2:
        while duplicated_gen_pos:
            temp = son1[duplicated_gen_pos]
            son1[duplicated_gen_pos] = son2[duplicated_gen_pos]
            son2[duplicated_gen_pos] = temp
            duplicated_gen_pos = duplicate_gene(son1, duplicated_gen_pos)

    return son1, son2


def mutation(son):
    son_i = random.randint(0, 19)
    son_j = random.randint(0, 19)
    son[son_i], son[son_j] = son[son_j], son[son_i]
    return son


def set_chromosome_fitness(matriz):
    for idx_row, chromosome in enumerate(matriz):
        list_of_distance = []
        for idx_col, gene in enumerate(chromosome):
            if idx_col == len(chromosome) - 1:
                # has to return to start
                dist = get_euclidian_distance(gene, matriz[idx_row][0])
            else:
                dist = get_euclidian_distance(gene, matriz[idx_row][idx_col + 1])

            list_of_distance.append(dist)

        chromosome_fitness.update({idx_row: get_fitness(list_of_distance)})


matriz = get_initial_possibilities()
count = 0
while count < 10000:
    total_population += len(matriz)
    count += 1
    set_chromosome_fitness(matriz)
    to_plot.append(chromosome_fitness.get(0))
    matriz = order_by_fitness(matriz, chromosome_fitness)
    fathers_1, fathers_2 = roulette(matriz)
    random.shuffle(fathers_1)
    random.shuffle(fathers_2)
    count2 = 0
    while count2 < 5:
        son1, son2 = crossing_over(fathers_1[count2], fathers_2[count2])
        son1 = mutation(son1)
        son2 = mutation(son2)
        matriz.append(son1)
        matriz.append(son2)
        count2 += 1


set_chromosome_fitness(matriz)
to_plot.append(chromosome_fitness.get(0))
matriz = order_by_fitness(matriz, chromosome_fitness)

print('Tamanho da População: ', 20)
print('Taxa de Mutação: ', 0.05)
print('Número de Cidades: ', 20)
print('Melhor Custo: ', chromosome_fitness.get(0), matriz[0])
print('Tamanho da População: ', total_population)

x = np.array(to_plot)
plt.plot(x)
plt.show()
