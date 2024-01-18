import numpy as np
import click

t1, t2 = int(input("Введите минимальную границу весов: ")), int(input("Максимальную границу: "))
matrix_dim = (int(input("Введите количество строк матрицы: ")), int(input("Количество столбцов: ")))

# t1 = 10
# t2 = 20
# matrix_dim = (7, 3)


matrix = np.random.randint(t1, t2, matrix_dim)

sums = [sum(row) for row in matrix]

dict_sums = dict(enumerate(sums))

dict_sorted = dict(sorted(dict_sums.items(), key=lambda x: x[1], reverse=True))

matrix_sorted = np.array([matrix[index] for index in dict_sorted.keys()])

# выводим исходную и отсортированную матрицы
print("Исходная матрица:\n", matrix)
print("Суммы строк матрицы:\n", dict_sums)

print("Отсортированная матрица:\n", matrix_sorted)
print("Суммы строк:\n", dict_sorted, "\n")

new_matrix = np.zeros(matrix_dim)
#print(new_matrix)

for i, row in enumerate(matrix_sorted):
    if i == 0:
        loc_min = min(row)
        ind = np.where(row == loc_min)
        # temp_arr = [ind[0][0], loc_min]
        print(ind[0][0], f" {loc_min}", sep=":", end="  ")
        new_matrix[i][ind[0][0]] += loc_min
        if i+1 != matrix_dim[0]:
            new_matrix[i+1] += new_matrix[i]
    else:
        loc_min = 9999
        min_index = 0
        min_el = 0
        for ind, elem in enumerate(row):
            temp_checked_elem = elem
            temp_sum = (new_matrix[i][ind] + elem) ** 2

            for indeex, element in enumerate(row):
                if element == temp_checked_elem:
                    continue
                else:
                    temp_sum += new_matrix[i][indeex] ** 2
            print(f"row number {i}, sum for element {elem} = {temp_sum}")
            if temp_sum < loc_min:
                loc_min = temp_sum
                min_index = ind
                min_el = elem
        print(f"adding element {min_el} to position {min_index}")
        new_matrix[i][min_index] += min_el
        if i+1 != matrix_dim[0]:
            new_matrix[i+1] += new_matrix[i]

click.pause()
print("\n", new_matrix)
print("Max = " , max(new_matrix[matrix_dim[0]-1]))

