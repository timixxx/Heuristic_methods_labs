import random
import click
from prettytable import PrettyTable


n = int(input("Введите количество процессоров: "))
m = int(input("Введите количество заданий: "))
minim, maxim = int(input("Введите минимальную границу весов: ")), int(input("Максимальную границу: "))
arr_tasks = []

for i in range(m):
    arr_tasks.append(random.randrange(minim, maxim))
# arr_tasks = [22, 5, 7, 14, 5, 5, 9, 7]  ---For Debug---


class Process:
    def __init__(self):
        self.sum = 0
        self.tasks = []


array_procs = []
for i in range(n):
    array_procs.append(Process())  # Creating array of processors

proc_ids = []
for i in range(n):
    id = f"Process #{i}"  # Creating a header for matrix
    proc_ids.append(id)

print("\n----------Unsorted matrix----------")
t = PrettyTable(proc_ids)
for task in arr_tasks:
    print_arr = []
    for i in range(n):
        print_arr.append(f"{task}")  # Printing unsorted matrix
    t.add_row(print_arr)

print(t)

arr_tasks.sort(reverse=True)  # sorting

print("\n----------Sorted matrix----------")
t = PrettyTable(proc_ids)
for task in arr_tasks:
    print_arr = []
    for i in range(n):
        print_arr.append(f"{task}")  # Printing sorted matrix
    t.add_row(print_arr)
print(t)

click.pause()  # Making pause for paper solving


def get_lower_process():  # function to choose a processor with least sum of weights
    least_proc_sum = 999
    least_proc = None
    for proc in array_procs:
        if proc.sum < least_proc_sum:
            least_proc_sum = proc.sum
            least_proc = proc
    return least_proc


def spread_tasks():  # function to spread tasks between processors
    counter = 0
    for task in arr_tasks:
        t = PrettyTable(['Process ID', 'Tasks', 'Summary'])
        iter = 0
        proc = get_lower_process()
        proc.tasks.append(task)
        proc.sum += task
        counter += 1
        for proc in array_procs:
            t.add_row([iter, proc.tasks, proc.sum])
            iter += 1
        if counter == len(arr_tasks):
            print("\n~~~~~~~~~Result~~~~~~~~~")
            print(t)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        else:
            print(f"Step #{counter}")
            print(t)


spread_tasks()

