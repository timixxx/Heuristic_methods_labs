import random
import click
from prettytable import PrettyTable


n = int(input("Введите количество процессоров: "))
m = int(input("Введите количество заданий: "))
minim, maxim = int(input("Введите минимальную границу весов: ")), int(input("Максимальную границу: "))

if n % 2 != 0:
    raise ValueError("Number of processes must be even!")

arr_tasks = []
# for i in range(m):
#     arr_tasks.append(random.randrange(minim, maxim))
arr_tasks = [21,20,20,19,18,17,17,16,14,12,11,11,10,10] # --for Debug--


class Process:
    def __init__(self):
        self.sum = 0
        self.tasks = []


proc_ids = []
for i in range(n):
    id = f"Process #{i}"
    proc_ids.append(id)
print("\n----------Unsorted matrix----------")
t = PrettyTable(proc_ids)
for task in arr_tasks:
    print_arr = []
    for i in range(n):
        print_arr.append(f"{task}")
    t.add_row(print_arr)

print(t)

arr_tasks.sort(reverse=True)
print("\n----------Sorted matrix----------")
t = PrettyTable(proc_ids)
for task in arr_tasks:
    print_arr = []
    for i in range(n):
        print_arr.append(f"{task}")
    t.add_row(print_arr)
print(t)

click.pause()


def get_lower_process(array_procs):
    least_proc_sum = 999
    least_proc = None
    for proc in array_procs:
        if proc.sum < least_proc_sum:
            least_proc_sum = proc.sum
            least_proc = proc
    return least_proc

results = []

def spread_tasks(arr_tasks, array_procs, start):
    counter = 0
    for task in arr_tasks:
        t = PrettyTable(['Process ID', 'Tasks', 'Summary'])
        iter = start

        proc = get_lower_process(array_procs)
        proc.tasks.append(task)
        proc.sum += task
        counter += 1
        for proc in array_procs:
            t.add_row([iter, proc.tasks, proc.sum])
            iter += 1
        if counter == len(arr_tasks):
            print("\n~~~~~~~~~Result~~~~~~~~~")
            print(t)
            results.append(t)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        else:
            print(f"Step #{counter}")
            print(t)



half_n = n//2

base_procs = []
secondary_procs_1 = []
secondary_procs_2 = []

for i in range(2):
    base_procs.append(Process())

for i in range(half_n):
    secondary_procs_1.append(Process())
    secondary_procs_2.append(Process())

print("\n==========First Level==========")
spread_tasks(arr_tasks, base_procs, 0)
print("\n==========Second Level=========")
spread_tasks(base_procs[0].tasks, secondary_procs_1, 0)
spread_tasks(base_procs[1].tasks, secondary_procs_2, half_n)

print("\n============Final Results============")
print("-----First Level-----\n", results[0], "\n", sep="")
print("-----Second Level-----\n", results[1], "\n", results[2], sep="")
# for res in results:
#     print(res, "\n")

