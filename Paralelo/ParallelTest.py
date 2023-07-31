from multiprocessing import Pool
import time
import Rappi2DB


def run_process(ids):
    Rappi2DB.to_db(ids[0], ids[1], ids[2])


num = 4965
num_proc = 3
base = num / num_proc
if int(base) == base:
    interval = [int(base)]
else:
    interval = [int(base), int(base) + 1]

i = 1
divs = []
for x in range(1, num_proc + 1):
    if x == num_proc:
        step = interval[-1] - 1
    else:
        step = interval[0] - 1
    divs.append((i, i + step, x))
    i = i + step + 1
divs = tuple(divs)
print(divs)

start_time = time.time()
print('Rappi Paralelo')
pool = Pool(processes=num_proc)
pool.map(run_process, divs)
elapsed_time = time.time() - start_time
print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
