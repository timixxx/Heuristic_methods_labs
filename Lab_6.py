import random

num_individuals = 11
processors = 5
min_number = 10
max_number = 25
population_size = 10
population = []
O_for_tour = []
best_copy = 11
crossover_rate = 0.55
mutation_rate = 0.6
count_years = 0
vector = []
best_count = 0
best_individual = -1

for i in range(processors):
    sub_b = []
    [sub_b.append(random.randint(min_number, max_number)) for _ in range(num_individuals)]
    vector.append(sub_b)


def create_O():
    O_new = [random.randint(0, int(255 / population_size))]
    [O_new.append(random.randint(0, 255)) for _ in range(len(vector[0][1:]))]
    population.append(O_new)


[create_O() for _ in range(population_size)]


def phenotype(genotype):
    global vector
    f_d = {}
    start = 255 // processors
    finish = 255
    step = 255 // processors
    for j in range(start, finish, step):
        f_d[j] = []
    if len(f_d.keys()) < processors:
        f_d[255] = []
    for i in range(len(genotype)):
        value = genotype[i]
        val_index = genotype.index(value)
        for j, index in zip(list(f_d.keys()), range(processors)):
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


def search_to_cross(O_parrent):
    check = population.index(O_parrent)
    i = random.randint(0, population_size - 1)
    j = random.randint(0, population_size - 1)
    while population[i] == O_parrent or population[j] == O_parrent or i == j:
        i = random.randint(0, population_size - 1)
        j = random.randint(0, population_size - 1)

    fenotype_i = phenotype(population[i])
    fenotype_j = phenotype(population[j])
    minmax_i = minmax(fenotype_i)
    minmax_j = minmax(fenotype_j)
    print(f"Второй родитель выбирался между особями: {i} и {j}")
    if minmax_i <= minmax_j:
        return population[i]
    else:
        return population[j]


def cross(O_parrent, second):
    O_new = []
    i = random.randint(1, num_individuals - 1)
    k = random.randint(1, num_individuals - 1)
    while k <= i:
        i = random.randint(1, num_individuals - 1)
        k = random.randint(1, num_individuals - 1)
    print(f'точки кроссовера = {i, k}')
    for j in range(0, i):
        O_new.append(O_parrent[j])
    for j in range(i, k):
        O_new.append(second[j])
    for j in range(k, num_individuals):
        O_new.append(O_parrent[j])
    # print(f'O -> {second} | {fenotype(second)}')
    return O_new


def mutation(O_cros):
    print('-----начало мутации-----')
    print(O_cros)
    i = random.randint(1, num_individuals - 1)
    print(f'Выбираем значение {O_cros[i]}')
    number = bin(O_cros[i])[2:]
    zeros = []
    [zeros.append(0) for _ in range(7 - len(number))]
    zeros = ''.join(map(str, zeros))
    number = zeros + number
    number = list(number)
    k = random.randint(0, len(number) - 1)
    j = random.randint(0, len(number) - 1)
    print(number)
    while j == k:
        j = random.randint(0, len(number) - 1)
    print(f'меняем местами биты = {k}, {j}')
    number[j], number[k] = number[k], number[j]
    number = ''.join(map(str, number))
    print(number)
    number = int(number, 2)
    O_cros[i] = number
    print('-----конец мутации-----')
    return O_cros


def print_matrix(d, gen_print=False):
    print('-------------')
    if gen_print:
        for i, itetarion in zip(d, range(len(d))):
            print(f"{itetarion} | {i} | нагрузка: {minmax(phenotype(i))}")
    else:
        for i, itetarion in zip(d, range(len(d))):
            print(f"{itetarion} | {i}")


def tournament(o_main, o_second):
    print(f'начало отбора лучших в поколении')
    print_matrix(o_main)
    print_matrix(o_second)
    o_all = o_main + o_second
    o_all = sorted(o_all, key=lambda o: minmax(phenotype(o)))
    print_matrix(o_all, True)
    o_new = o_all[:len(o_main)]
    print('конец отбора лучших в поколении')
    return o_new


print('Матрица нагрузок:')
print_matrix(vector)
print("Исходная популяция:")
print_matrix(population, True)

for cur in population:
    if best_individual == -1:
        best_individual = minmax(phenotype(cur))
    elif best_individual > minmax(phenotype(cur)):
        best_individual = minmax(phenotype(cur))
print("Лучшая особь:", best_individual)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
while best_count < best_copy - 1:
    count_years += 1
    print(f'------Поколение №{count_years}------')
    # выбираем лучшую особь
    print('Матрица нагрузок:')
    print_matrix(vector)
    new_population = []
    print('Текущее поколение:')
    print_matrix(population, True)
    print()
    for cur, iteration in zip(population, range(1, len(population) + 1)):
        second_individ = search_to_cross(cur)
        new_1 = cross(cur, second_individ)
        new_2 = cross(second_individ, cur)

        if random.random() > crossover_rate:
            print('Кроссовер не произошел')
            new_1 = cur
            new_2 = cur
        else:
            print("Произошел кроссовер")
        if random.random() < mutation_rate:
            print(f"Произошла мутация 1-го потомка:")
            print(f"{new_1} | {phenotype(new_1)}| нагрузка: {minmax(phenotype(new_1))}")
            new_1 = mutation(new_1.copy())
            print(f"{new_1} | {phenotype(new_1)}| нагрузка: {minmax(phenotype(new_1))}")

        else:
            print('Мутация 1-го потомка не произошла')

        if random.random() > mutation_rate:
            print(f"Произошла мутация 2-го потомка:")
            print(f"{new_2} | {phenotype(new_2)} | нагрузка: {minmax(phenotype(new_2))}")
            new_2 = mutation(new_2.copy())
            print(f"{new_2} | {phenotype(new_2)}| нагрузка: {minmax(phenotype(new_2))}")
        else:
            print('Мутация 2-го потомка не произошла')

        print(f"1-й родитель = {cur} | {phenotype(cur)} | {minmax(phenotype(cur))}")
        print(f"2-й родитель = {second_individ} | {phenotype(second_individ)} | {minmax(phenotype(second_individ))}")
        print(f"1-й потомок = {new_1} | {phenotype(new_1)} | {minmax(phenotype(new_1))}")
        print(f"2-й потомок = {new_2} | {phenotype(new_2)} | {minmax(phenotype(new_2))}")
        dic = {
            minmax(phenotype(new_1)): new_1,
            minmax(phenotype(new_2)): new_2,
            minmax(phenotype(cur)): cur
        }
        minmax_matrix = min([minmax(phenotype(new_1)),
                             minmax(phenotype(new_2)),
                             minmax(phenotype(cur))])
        print(f"\nЛучшая особь (в новое) {dic[minmax_matrix]} | нагрузка: {minmax_matrix}\n"
              f"~~~~~~~~~~~~~~~~~~~~~~Итерация #{iteration}~~~~~~~~~~~~~~~~~~~~~~")
        O_for_tour.append(dic[minmax_matrix])  # добавляем лучшую особь в отдельный массив
        new_population.append(dic[minmax_matrix])
    if len(population) == len(O_for_tour):
        population = tournament(population, O_for_tour)
        O_for_tour = []
    list_for_minmax = []
    [list_for_minmax.append(minmax(phenotype(population[i]))) for i in range(len(population))]
    minmax_matrix = min(list_for_minmax)
    if best_individual <= minmax_matrix:
        best_count += 1
    else:
        best_count = 0

    for cur in population:
        if best_individual == -1:
            best_individual = minmax(phenotype(cur))
        elif best_individual > minmax(phenotype(cur)):
            best_individual = minmax(phenotype(cur))
    print("Лучшая особь поколения:", best_individual)
    print('++++++++++++++++++++++++++++++++++++++++++++++')
