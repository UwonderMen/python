import asyncio
import inspect

@asyncio.coroutine
def sleep(x):
    for i in range(3):
        print("sleep {}".format(i))
        yield from asyncio.sleep(x)

@asyncio.coroutine
def do(x):
    for i in range(3):
        print("do {}".format(i))
        yield from asyncio.sleep(x)

asyncio.start_server()
print(inspect.iscoroutinefunction(sleep))
print(inspect.iscoroutinefunction(do))
loop = asyncio.get_event_loop()
tasks = [sleep(2),do(2)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# async def do(x):
#     for i in range(3):
#         print("sleep {}".format(i))
#         await asyncio.sleep(x)
