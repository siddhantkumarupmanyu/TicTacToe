import asyncio
import datetime


async def hello_world():
    print("Hello world")


async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))
    return f


async def parallelExecution():
    results = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    for result in results:
        print(f"result:- {result}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete(hello_world())
    loop.run_until_complete(display_date(loop))
    loop.run_until_complete(print_sum(1, 2))

    loop.run_until_complete(parallelExecution())

    loop.close()

# more info https://docs.python.org/3.6/library/asyncio-task.html
# https://docs.python.org/3.6/library/asyncio-task.html#example-parallel-execution-of-tasks
