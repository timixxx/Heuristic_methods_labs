import networkx as nx
import matplotlib.pyplot as plt
import random


start_node = 7
processors = 11  # N (кол-во вершин)
min_num = 10
max_num = 20
num_individuals = 10  # M
num_repeats = 10
crossover_rate = 100
mutation_rate = 100

mutation_rate = mutation_rate / 100
crossover_rate = crossover_rate / 100


def probability(probability, str):
    if random.random() < probability:
        print("Произошел(а) " + str)
        return True
    else:
        print("Не произошел(а) " + str)
        return False


def myWay(way, arr):
    Sum_way = 0
    for i in range(len(way)-1):
        Sum_way += arr[way[i]][way[i+1]]
    return Sum_way


def genetic(graph, P_cross, P_mutant, arr):
    for i in range(len(graph)):
        print("\n")
        if probability(P_cross, "Кроссовер"):
            row = (lambda x, y=i: x + 1 if x >= y else x)(random.randint(0, len(graph) - 2))
            print(f"O{i}: {graph[i]} = {myWay(graph[i], arr)}\nO{row}: {graph[row]} = {myWay(graph[row], arr)}")
            matrix = [list(graph[i]), list(graph[row])]
            point = random.randint(1, len(graph[i]) - 2)
            print(f"Точка кроссовера = {point}")
            tmatrix0 = matrix[0][:point]
            tmatrix1 = matrix[1][:point]

            for g in matrix[1]:
                if g not in tmatrix0:
                    tmatrix0.append(g)
            for g in matrix[0]:
                if g not in tmatrix1:
                    tmatrix1.append(g)
            matrix[0][point:len(tmatrix0)] = tmatrix0[point:len(tmatrix0)]
            matrix[1][point:len(tmatrix1)] = tmatrix1[point:len(tmatrix1)]
            print(f"П1 = {matrix[0]} = {myWay(matrix[0],arr)}\nП2 = {matrix[1]} = {myWay(matrix[1],arr)}")
            if probability(P_mutant, "Мутация"):
                for j in range(len(matrix)):
                    point0 = random.randint(1, len(matrix[j]) - 2)
                    point1 = (lambda x, y=point0: x + 1 if x >= y else x)(random.randint(1, len(matrix[j]) - 3))
                    matrix[j][point0], matrix[j][point1] = (matrix[j][point1], matrix[j][point0])
                    print(f"П{j+1}: меняются местами {point0} и {point1}\n{matrix[j]} = {myWay(matrix[j],arr)}")
            if myWay(graph[i], arr) < myWay(matrix[0], arr) and myWay(matrix[1], arr):
                print(f"O{i} = {myWay(graph[i],arr)} < П1 и П2")
            elif myWay(matrix[0], arr) < myWay(matrix[1], arr):
                print("П1 < П2")
                graph[i] = matrix[0]
            else:
                print("П2 <= П1")
                graph[i] = matrix[1]
        else:
            print(f"O{i} := {graph[i]} = {myWay(graph[i], arr)}")
            if probability(P_mutant, "мутация"):
                point0 = random.randint(1, len(graph[i]) - 2)
                point1 = (lambda x, y=point0: x + 1 if x >= y else x)(random.randint(1, len(graph[i]) - 3))
                matrix = list(graph[i])
                matrix[point0], matrix[point1] = (matrix[point1], matrix[point0])
                print(f"П{1}: меняем местами {point0} и {point1}\n{matrix} = {myWay(matrix, arr)}")
                if myWay(matrix, arr) < myWay(graph[i], arr):
                    graph[i] = list(matrix)
                    print(f"П1 < O{i} = {myWay(graph[i], arr)}")
                else:
                    print(f"O{i} = {myWay(graph[i], arr)} <= П1")
    return


def tsp_greedy(graph, start_node):
    num_nodes = len(graph)
    path = [start_node]
    visited = [False] * num_nodes
    visited[start_node] = True  # Помечаем начальную вершину как посещенную

    while len(path) < num_nodes:
        current_node = path[-1]
        min_distance = float('inf')
        next_node = None

        for neighbor in range(num_nodes):
            if not visited[neighbor] and graph[current_node][neighbor] < min_distance:
                min_distance = graph[current_node][neighbor]
                next_node = neighbor

        path.append(next_node)
        visited[next_node] = True

    path.append(start_node)  # Замыкаем путь
    total_distance = sum(graph[path[i]][path[i + 1]] for i in range(num_nodes))

    return path, total_distance


def draw_tsp_graph(graph, path, color):
    num_nodes = len(graph)
    G = nx.Graph()

    for i in range(num_nodes):
        G.add_node(i)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = graph[i][j]
            if weight != 0:
                G.add_edge(i, j, weight=weight)

    pos = nx.circular_layout(G)

    # Рисование графа
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue')

    # Рисование пути
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    path_edges.append((path[-1], path[0]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=color, width=2.0)

    # Вывод весов на ребрах
    edge_labels = {(u, v): str(graph[u][v]) for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


def initialize_diagonal(matrix):
    n = len(matrix)
    for i in range(n):
        matrix[i][i] = 0
    return matrix


graph = [[random.randint(min_num, max_num) for j in range(processors)] for i in range(processors)]
graph = initialize_diagonal(graph)

for i in range(len(graph[0])):
    for j in range(len(graph[0])-i):
        graph[j+i][i] = graph[i][j+i]


array = []
for _ in range(num_individuals):
    row = list(range(0, processors))
    del row[start_node]
    random.shuffle(row)
    array.append([start_node] + row + [start_node])

print("\n-----Матрица значений-----")
for row in graph:
    print(row)


bests = []
count = 1

while True:
    min_gens = []
    print(f"------Поколение №{len(bests)}------")
    for i in range(len(array)):
        min_gens.append(myWay(array[i], graph))
        print(f"O{i}: {array[i]} = {min_gens[i]}")
    bests.append(min(min_gens))
    print(f"Минимальная нагрузка = {bests[len(bests) - 1]}")
    if count == num_repeats:
        for i in range(len(bests)):
            print(f"Минимальная длина пути {i}-й особи = {bests[i]}")
        break
    elif bests[len(bests) - 1] == bests[len(bests) - 2]:
        count = count + 1
    else: count = 1
    genetic(array, crossover_rate, mutation_rate, graph)

# print("\n-----Матрица значений-----")
# for row in graph:
#     print(row)

# жадный алгоритм
path, distance = tsp_greedy(graph, start_node)
print("\nМинимальный путь жадного алгоритма:", path)
print("Минимальное расстояние жадного алгоритма:", distance)
draw_tsp_graph(graph, path, 'blue')

# генетический алгоритм
for row in array:
    if bests[len(bests) - 1] == myWay(row, graph):
        path = row
        break
draw_tsp_graph(graph, path, 'green')