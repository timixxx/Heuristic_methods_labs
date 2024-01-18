import numpy as np
import click

t1, t2 = int(input("Введите минимальную границу заданий: ")), int(input("Максимальную границу: "))
n, m = int(input("Введите количество устройств (n): ")), int(input("Количество работ (m): "))
# t1, t2, n, m = 4, 22, 4, 7

works = np.random.randint(t1, t2, m)
print("Исходный вектор заданий:\n", works, sep="")
# works = [5, 10, 15, 7, 4, 22, 5]
devices = [[] for i in range(n)]


def random_input():
    for num, w in enumerate(works):
        i = np.random.randint(0, n)
        devices[i].append(w)
        print(f"Случайным образом добавляем элемент {w} в прибор {i}\n {devices}")


def get_lower_process(devices):  # function to choose a processor with least sum of weights
    least_proc_sum = 999
    least_proc = None
    for proc in devices:
        if sum(proc) < least_proc_sum:
            least_proc_sum = sum(proc)
            least_proc = proc
    return least_proc


def CMP_input():
    for num, w in enumerate(works):
        least_process = get_lower_process(devices)
        least_process.append(w)
        print(f"CMP методом добавляем элемент {w} в прибор {devices.index(least_process)}\n {devices}")


#devices = [[13], [10, 17, 14, 10, 12, 12, 12], [13], [15, 16]]


def crone(devices, sort=False):
    do_step = True
    do_again = False
    while do_step or do_again:
        if sort:
            for process in devices:
                process.sort(reverse=True)
            print(f"Сортируем приборы по убыванию...\n {devices}")
        sums = [sum(lst) for lst in devices]
        max_index = sums.index(max(sums))
        min_index = sums.index(min(sums))

        max_device = devices[max_index]
        min_device = devices[min_index]

        max_sum = max(sums)
        min_sum = min(sums)

        print(f"\nПрибор с максимальной загруженностью №{max_index}:", max_device, f"Суммарная загрузка = {max_sum}")
        print(f"Прибор с минимальной загруженностью №{min_index}:", min_device, f"Суммарная загрузка = {min_sum}")

        delta = max_sum - min_sum
        print(f"delta: {max_sum} - {min_sum} = {delta}")
        for index, task in enumerate(devices[max_index]):
            if task < delta:
                print(f"Перемещаем элемент {task} из прибора {max_device} в прибор {min_device}")
                temp = devices[max_index].pop(index)
                devices[min_index].append(temp)
                do_step = True
                break
            elif task == devices[max_index][-1]:
                print("Нет элементов, которые меньше delta. Конец перестановок\n")
                do_step = False

        print("Распределение заданий после перестановок приборов:\n", devices, sep="")

        sums = [sum(lst) for lst in devices]
        max_index = sums.index(max(sums))
        min_index = sums.index(min(sums))
        max_sum = max(sums)
        min_sum = min(sums)
        delta = max_sum - min_sum
        do_again = False
        for index, task in enumerate(devices[max_index]):
            for low_task in devices[min_index]:
                if task > low_task and task - low_task < delta and do_step == False:
                    low_index = devices[min_index].index(low_task)
                    high_index = devices[max_index].index(task)
                    temp = task
                    devices[max_index][high_index] = low_task
                    devices[min_index][low_index] = temp
                    # temp = devices[max_index].pop(index)
                    # devices[min_index].append(temp)
                    print("Перемещаем элемент:", task)
                    do_again = True
                    break
                else:
                    do_again = False

    print("Распределение заданий после перебора:\n", devices, sep="")
    # if do_again:
    #     crone(devices, sort=True)
    sums = [sum(lst) for lst in devices]
    max_index = sums.index(max(sums))
    max_sum = max(sums)
    print(f"\nМаксимальное время завершения работ в приборе №{max_index} = {max_sum}")


#random_input()
CMP_input()
click.pause()
crone(devices, sort=False)
