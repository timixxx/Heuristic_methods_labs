import numpy as np
import pandas as pd
import random

M = 8
N = 3
T1 = 10
T2 = 22
O_count = 6
O = []
best_copy = 10
p_cros = 0.01
p_mut = 0.8
# M, N = int(input('M= ')), int(input('N= '))
# T1, T2 = int(input('Tmin= ')), int(input('Tmax= '))
# O_count = int(input('число особей= '))
# best_copy = int(input('кол-во повторений = '))
count_years = 0
# vector = np.array([10, 12, 16, 18, 17, 10, 13, 19])

vector = []
[vector.append(random.randint(T1, T2)) for _ in range(M)]


# p_cros = float(input('p_cros = '))
# p_mut = float(input('p_mut = '))


def create_O():
    O_new = [random.randint(0, int(255 / O_count))]
    [O_new.append(random.randint(0, 255)) for _ in vector[1:]]
    O.append(O_new)


def print_O(d):
    # print(vector)
    for i in d:
        print(i)


[create_O() for _ in range(O_count)]
print(vector)
print_O(O)


# из генотипа в фенотип

def fenotype(genotype):
    f = {}
    start = 255 // N
    finish = 255
    step = 255 // N
    for j in range(start, finish, step):
        f[j] = []
    if len(f.keys()) < N:
        f[255] = []
    for i in range(len(genotype)):
        value = genotype[i]
        for j in list(f.keys()):
            if value <= j:
                f[j].append(vector[genotype.index(value)])
                break
    sum_f = []
    [sum_f.append(sum(f.get(i))) for i in f]
    print(f"{sum_f} -----")
    return max(sum_f)


def cross(O_parrent, second=None):
    O_new = []
    i = random.randint(0, O_count - 1)
    if second is None:
        while O[i] == O_parrent:
            i = random.randint(0, O_count - 1)
        second = O[i]
    i = random.randint(1, M - 1)
    for j in range(0, i):
        O_new.append(O_parrent[j])
    for j in range(i, M):
        O_new.append(second[j])
    print(f'O -> {second} | {fenotype(second)}')
    return O_new, second


def mutation(O_cros):
    i = random.randint(0, M - 1)
    number = bin(O_cros[i])[2:]
    zeros = []
    [zeros.append(0) for _ in range(7 - len(number))]
    zeros = ''.join(map(str, zeros))
    number = zeros + number
    j = random.randint(0, len(number) - 1)
    number = list(number)
    if int(number[j]):
        number[j] = 0
    else:
        number[j] = 1
    number = ''.join(map(str, number))
    number = int(number, 2)
    O_cros[i] = number
    return O_cros


# mutation(O[0])

best_count = 0
best_individual = -1
# def minmax():
#     list_forminmax = []
#     [list_forminmax.append(fenotype(i)) for i in O]
#     best_minmax = max(list_forminmax) - min(list_forminmax)


for cur in O:
    if best_individual == -1:
        best_individual = fenotype(cur)
    elif best_individual > fenotype(cur):
        best_individual = fenotype(cur)
print(best_individual)
print('=========================================================================================')
while best_count < best_copy - 1:
    count_years += 1
    print(f'Поколение №{count_years}')
    # выбираем лучшую особь
    print(f"{vector} <- vector")
    new_O = []
    print('Данное поколоние ->')
    print_O(O)
    print()
    for cur, itearte in zip(O, range(1, len(O) + 1)):
        # index_cross = O.index(cur)
        # while index_cross == O.index(cur):
        #     index_cross = random.randint(0, len(O) - 1)
        # o_cross = O[index_cross]
        new_1, O_second = cross(cur)
        new_2, _ = cross(O_second, cur)
        if random.random() > p_cros:
            print('кросс отсутвует')
            new_1 = cur
            new_2 = cur
        if random.random() < p_mut:
            new_1 = mutation(new_1.copy())

        else:
            print('мутация отсутвует1')
        print(f"1-ый потомок -> {new_1} | {fenotype(new_1)}")
        # new_2, _ = cross(O_second, cur)
        # if random.random() < p_cros:
        #     print('кросс отсутвует')
        #     new_2 = cur
        if random.random() > p_mut:
            new_2 = mutation(new_2.copy())
        else:
            print('мутация отсутвует2')

        print(f"2-ый потомок -> {new_2} | {fenotype(new_2)}")
        dic = {
            fenotype(new_1): new_1,
            fenotype(new_2): new_2,
            fenotype(cur): cur
        }
        minmax = min([fenotype(new_1), fenotype(new_2), fenotype(cur)])
        print(f"\nидёт в новое поколение -> {dic[minmax]} - {minmax}\n"
              f"{itearte}----------------------------------------------------------------{itearte}")

        new_O.append(dic[minmax])
    O = new_O
    list_for_minmax = []
    [list_for_minmax.append(fenotype(O[i])) for i in range(len(O))]
    minmax = min(list_for_minmax)
    if best_individual <= minmax:
        best_count += 1
    else:
        best_count = 0

    for cur in O:
        if best_individual == -1:
            best_individual = fenotype(cur)
        elif best_individual > fenotype(cur):
            best_individual = fenotype(cur)
    print(best_individual)
    print('=========================================================================================')

# minmax = min([fenotype(O[0]), fenotype(O[1]), fenotype(O[2])])
# dic = {}
# print(minmax)
# print(dic[minmax])
