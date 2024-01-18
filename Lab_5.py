import random

num_individuals = 12  # M
processors = 5  # N
min_number = 10
max_number = 22
population_size = 11
population = []
best_copy = 11
crossover_rate = 0.65
mutation_rate = 0.70
count_years = 0


vector = []
[vector.append(random.randint(min_number, max_number)) for _ in range(num_individuals)]


def create_population():
    O_new = [random.randint(0, int(255 / population_size))]
    [O_new.append(random.randint(0, 255)) for _ in vector[1:]]
    population.append(O_new)


def print_population(d):
    for i in d:
        print(i)


[create_population() for _ in range(population_size)]
print("Исходная матрица значений:", vector)
print_population(population)


# из генотипа в фенотип

def phenotype(genotype, to_print = False):
    f = {}
    start = 255 // processors
    finish = 255
    step = 255 // processors
    for j in range(start, finish, step):
        f[j] = []
    if len(f.keys()) < processors:
        f[255] = []
    for i in range(len(genotype)):
        value = genotype[i]
        for j in list(f.keys()):
            if value <= j:
                f[j].append(vector[genotype.index(value)])
                break
    sum_f = []
    [sum_f.append(sum(f.get(i))) for i in f]
    if to_print:
        print(f"Нагрузки процессоров: {sum_f}")
    return max(sum_f)


def cross(population_parent, second=None):
    O_new = []
    i = random.randint(0, population_size - 1)
    if second is None:
        while population[i] == population_parent:
            i = random.randint(0, population_size - 1)
        second = population[i]
    i = random.randint(1, num_individuals - 1)
    for j in range(0, i):
        O_new.append(population_parent[j])
    for j in range(i, num_individuals):
        O_new.append(second[j])
    print(f'Родитель = {second} | нагрузка: {phenotype(second)}')
    return O_new, second


def mutation(O_cros):
    i = random.randint(0, num_individuals - 1)
    print(f"Изменяется элемент №{i} = {O_cros[i]}")
    number = bin(O_cros[i])[2:]
    zeros = []
    [zeros.append(0) for _ in range(7 - len(number))]
    zeros = ''.join(map(str, zeros))
    number = zeros + number
    j = random.randint(0, len(number) - 1)
    number = list(number)
    print(f"Порядковый номер изменяемого бита #{j}")
    print(f"До = {number}")
    if int(number[j]):
        number[j] = 0
    else:
        number[j] = 1
    print(f"После = {number}")
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


for cur in population:
    if best_individual == -1:
        best_individual = phenotype(cur, True)
    elif best_individual > phenotype(cur, True):
        best_individual = phenotype(cur)
print("Лучшая особь:", best_individual)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
while best_count < best_copy - 1:
    count_years += 1
    print(f'------Поколение №{count_years}------')
    # выбираем лучшую особь
    #print(f"{vector} <- vector")
    new_population = []
    print('Текущее поколение:')
    print_population(population)
    print()
    for cur, iter in zip(population, range(1, len(population) + 1)):
        new_1, O_second = cross(cur)
        new_2, _ = cross(O_second, cur)
        if random.random() > crossover_rate:
            print('Кроссовер не произошел, "потомки" = родители')
            new_1 = cur
            new_2 = cur
        else:
            print("Кроссовер произошел")
        if random.random() < mutation_rate:
            print(f"Произошла мутация 1-го потомка:")
            print(f"{new_1} | нагрузка: {phenotype(new_1, True)}")
            new_1 = mutation(new_1.copy())
            print(new_1)

        else:
            print('Мутация 1-го потомка не произошла')
        print(f"1-й потомок = {new_1} | нагрузка: {phenotype(new_1, True)}")

        if random.random() > mutation_rate:
            print(f"Произошла мутация 2-го потомка:")
            print(f"{new_2} | нагрузка: {phenotype(new_2, True)}")
            new_2 = mutation(new_2.copy())
            print(new_2)
        else:
            print('Мутация 2-го потомка не произошла')

        print(f"2-й потомок = {new_2} | нагрузка: {phenotype(new_2, True)}")
        dic = {
            phenotype(new_1): new_1,
            phenotype(new_2): new_2,
            phenotype(cur): cur
        }
        minmax = min([phenotype(new_1, True), phenotype(new_2, True), phenotype(cur, True)])
        print(f"\nЛучшая особь = {dic[minmax]} | нагрузка: {minmax}\n"
              f"~~~~~~~~~~~~~~~~~~~~~~Итерация #{iter}~~~~~~~~~~~~~~~~~~~~~~")

        new_population.append(dic[minmax])
    population = new_population
    list_for_minmax = []
    [list_for_minmax.append(phenotype(population[i])) for i in range(len(population))]
    minmax = min(list_for_minmax)
    if best_individual <= minmax:
        best_count += 1
    else:
        best_count = 0

    for cur in population:
        if best_individual == -1:
            best_individual = phenotype(cur, True)
        elif best_individual > phenotype(cur, True):
            best_individual = phenotype(cur)
    print("Лучшая особь поколения:", best_individual)
    print('----------------------------------')

