import concurrent
import time
from concurrent.futures.thread import ThreadPoolExecutor


def sleepFor(seconds: int):
    time.sleep(seconds)
    print(f"seconds {seconds} done")
    return f"seconds {seconds} done"


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(5):
            futures.append(executor.submit(sleepFor, seconds=6-i))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

# more info https://docs.python.org/3/library/concurrent.futures.html
# https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future
# https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
