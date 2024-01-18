import random

M = 11
N = 4
T1 = 10
T2 = 25
O_count = 11
O = []
O_for_tour = []
best_copy = 11
p_cros = 0.6
p_mut = 0.7
count_years = 0
vector = []
best_count = 0
best_individual = -1

for i in range(N):
    sub_b = []
    [sub_b.append(random.randint(T1, T2)) for _ in range(M)]
    vector.append(sub_b)


def create_O():
    O_new = [random.randint(0, int(255 / O_count))]
    [O_new.append(random.randint(0, 255)) for _ in range(len(vector[0][1:]))]
    O.append(O_new)


[create_O() for _ in range(O_count)]


def fenotype(genotype):
    global vector
    f_d = {}
    start = 255 // N
    finish = 255
    step = 255 // N
    for j in range(start, finish, step):
        f_d[j] = []
    if len(f_d.keys()) < N:
        f_d[255] = []
    for i in range(len(genotype)):
        value = genotype[i]
        val_index = genotype.index(value)
        for j, index in zip(list(f_d.keys()), range(N)):
            if value <= j:
                f_d[j].append(vector[index][i])
                break
    return f_d


def minmax(dict_f):
    if isinstance(dict_f, dict):
        sum_f = []
        [sum_f.append(sum(dict_f.get(i))) for i in dict_f]
        # print(f"{sum_f} -> разгрузка")
        return max(sum_f)


def find_for_sex(O_parrent):
    check = O.index(O_parrent)
    i = random.randint(0, O_count - 1)
    j = random.randint(0, O_count - 1)
    while O[i] == O_parrent or O[j] == O_parrent or i == j:
        i = random.randint(0, O_count - 1)
        j = random.randint(0, O_count - 1)

    fenotype_i = fenotype(O[i])
    fenotype_j = fenotype(O[j])
    minmax_i = minmax(fenotype_i)
    minmax_j = minmax(fenotype_j)
    print(f"выбирались среди родителей под индексами {i} и {j}")
    if minmax_i <= minmax_j:
        return O[i]
    else:
        return O[j]


def cross(O_parrent, second):
    O_new = []
    i = random.randint(1, M - 1)
    k = random.randint(1, M - 1)
    while k <= i:
        i = random.randint(1, M - 1)
        k = random.randint(1, M - 1)
    print(f'токчи кроссовера - {i, k}')
    for j in range(0, i):
        O_new.append(O_parrent[j])
    for j in range(i, k):
        O_new.append(second[j])
    for j in range(k, M):
        O_new.append(O_parrent[j])
    # print(f'O -> {second} | {fenotype(second)}')
    return O_new


def mutation(O_cros):
    # print('начало мутации------------')
    # print(O_cros)
    i = random.randint(1, M - 1)
    # print(f'Выбираем {O_cros[i]}')
    number = bin(O_cros[i])[2:]
    zeros = []
    [zeros.append(0) for _ in range(7 - len(number))]
    zeros = ''.join(map(str, zeros))
    number = zeros + number
    number = list(number)
    k = random.randint(0, len(number) - 1)
    j = random.randint(0, len(number) - 1)
    # print(number)
    while j == k:
        j = random.randint(0, len(number) - 1)
    # print(f'change - {k}, {j}')
    number[j], number[k] = number[k], number[j]
    number = ''.join(map(str, number))
    # print(number)
    number = int(number, 2)
    O_cros[i] = number
    # print('конец мутации------------')
    return O_cros


def print_matrix(d, gen=False):
    # print(vector)
    print('----------------------------------')
    for i, itetarion in zip(d, range(len(d))):
        print(f"{itetarion} |{i}| {minmax(fenotype(i))}")


def tournament(o_main, o_second):
    print(f'начало турнира')
    print_matrix(o_main)
    print_matrix(o_second)
    o_all = o_main + o_second
    o_all = sorted(o_all, key=lambda o: minmax(fenotype(o)))
    print_matrix(o_all, True)
    o_new = o_all[:len(o_main)]
    print('конец турнира')
    return o_new


print_matrix(vector)
print_matrix(O)

for cur in O:
    if best_individual == -1:
        best_individual = minmax(fenotype(cur))
    elif best_individual > minmax(fenotype(cur)):
        best_individual = minmax(fenotype(cur))
print(best_individual)
print('=========================================================================================')
while best_count < best_copy - 1:
    count_years += 1
    print(f'Поколение №{count_years}')
    # выбираем лучшую особь
    print('матрица нагрузок ->')
    print_matrix(vector)
    new_O = []
    print('Данное поколоние ->')
    print_matrix(O, True)
    print()
    for cur, itearte in zip(O, range(1, len(O) + 1)):
        # index_cross = O.index(cur)
        # while index_cross == O.index(cur):
        #     index_cross = random.randint(0, len(O) - 1)
        # o_cross = O[index_cross]
        O_second = find_for_sex(cur)
        new_1 = cross(cur, O_second)
        new_2 = cross(O_second, cur)

        if random.random() > p_cros:
            print('кросс отсутвует')
            new_1 = cur
            new_2 = cur
        if random.random() < p_mut:
            new_1 = mutation(new_1.copy())

        else:
            print('мутация отсутвует1')

        if random.random() > p_mut:
            new_2 = mutation(new_2.copy())
        else:
            print('мутация отсутвует2')

        fenotypy_cur = fenotype(cur)
        fenotypy_O_second = fenotype(O_second)
        fenotypy_new_1 = fenotype(new_1)
        fenotypy_new_2 = fenotype(new_2)
        print(f"1_ый родитель -> {cur} | {fenotypy_cur} | {minmax(fenotypy_cur)}")
        print(f"2_ый родитель -> {O_second} | {fenotypy_O_second} | {minmax(fenotypy_cur)}")
        print(f"1_ый потомок -> {new_1} | {fenotypy_new_1} | {minmax(fenotypy_new_1)}")
        print(f"1_ый потомок -> {new_2} | {fenotypy_new_2} | {minmax(fenotypy_new_2)}")
        dic = {
            minmax(fenotype(new_1)): new_1,
            minmax(fenotype(new_2)): new_2,
            minmax(fenotype(cur)): cur
        }
        minmax_matrix = min([minmax(fenotype(new_1)),
                             minmax(fenotype(new_2)),
                             minmax(fenotype(cur))])
        print(f"\nидёт в новое поколение -> {dic[minmax_matrix]} - {minmax_matrix}\n"
              f"{itearte}----------------------------------------------------------------{itearte}")
        O_for_tour.append(dic[minmax_matrix])
        new_O.append(dic[minmax_matrix])
    if len(O) == len(O_for_tour):
        O = tournament(O, O_for_tour)
    list_for_minmax = []
    [list_for_minmax.append(minmax(fenotype(O[i]))) for i in range(len(O))]
    minmax_matrix = min(list_for_minmax)
    if best_individual <= minmax_matrix:
        best_count += 1
    else:
        best_count = 0

    for cur in O:
        if best_individual == -1:
            best_individual = minmax(fenotype(cur))
        elif best_individual > minmax(fenotype(cur)):
            best_individual = minmax(fenotype(cur))
    print(best_individual)
    print('=========================================================================================')
