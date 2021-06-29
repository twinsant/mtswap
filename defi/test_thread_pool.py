import concurrent.futures
import time

def high_load_work(i):
    print('{} doing...'.format(i))
    time.sleep(3)
    return i

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for i in range(100):
        futures.append(executor.submit(high_load_work, i))
    for future in concurrent.futures.as_completed(futures):
        i = future.result()
        print('{} done'.format(i))